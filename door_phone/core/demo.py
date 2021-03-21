import os
import time
import threading
import requests
import pyaudio
import numpy as np
import anal
import json
import websocket
try:
    import thread
except ImportError:
    import _thread as thread

from core import config
from core import message
from core import preprocessing
from core import record
from core import speech_synth


class AudioStateInfo:
    def __init__(self):
        self.n_up_edge: int = 0
        self.n_down_edge: int = 0
        self.current_vol: float = 0
        self.total_vol: float = 0
        self.average_vol: float = 0
        self.border: float = 9999
        self.n_sample: int = 0


class Demo:
    def __init__(self):
        self.recorder: record.Record = record.Record()

        self.stream: pyaudio.Stream = self.recorder.pa.open(
            format=pyaudio.paFloat32,
            channels=config.WAVE_CHANNELS,
            rate=config.WAVE_RATE,
            input=True,
            output=False,
            frames_per_buffer=config.WAVE_CHUNK,
        )

        # analyzer in stdout
        self.anal: anal.Anal = anal.Anal('config/demo.txt.anal')

        # detection params
        self.audio_state: AudioStateInfo = AudioStateInfo()
        self.reset_state_interval: float = 0.3
        self.past_time: time.time = time.time()
        self.record_start_time: time.time

        self.is_confirm: bool = False
        self.is_recording: bool = False
        self.enable_detect: bool = False
        self.block_detect: bool = True
        self.is_exit: bool = False

        self.pred_class: str = ''
        self.log_message: str = ''

        # create web socket object
        self.ws_app = websocket.WebSocketApp(
            config.INTERMEDIATE_SERVER_URL,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        self.ws_app.on_open = self.on_open
        self.ws_app.run_forever()

    def start(self):
        # update border in sub-thread
        thread: threading.Thread = \
            threading.Thread(target=self.update_border)
        thread.start()

        self.synthesiser = speech_synth.SpeechSynth()
        # """
        rules: dict = {
            "1": "友人、知人",
            "2": "宅配業者",
            "3": "NHK",
            "4": "宗教勧誘",
            "5": "ウーバーイーツ",
        }
        for cmd in rules:
            text: str = "%sのかたは%sを" % (rules[cmd], cmd)
            self.log_message = message.PLAY_AUDIO_MSG(text)
            self.draw_field()
            self.synthesiser.play(text)
        self.synthesiser.play("選択してください")
        # """

        # start to detect
        self.detect_loop()

    def detect_loop(self):
        self.enable_detect: bool = True
        self.block_detect = False
        self.audio_state.border += 2000
        self.past_time = time.time()

        while not self.is_exit:
            try:
                if time.time() - self.past_time > self.reset_state_interval:
                    self.reset_audio_state()

                if not self.block_detect:
                    self.audio_state.n_sample += 1
                    self.detection()
                self.draw_field()

                if self.is_recording:
                    self.recorder.start()
                else:
                    self.recorder.stop()

                if not self.enable_detect:
                    self.recorder.save(config.RECORD_WAV_PATH)

                    self.pred_class = self.predict()
                    if not self.is_confirm:
                        self.ws_app.send(
                            '{"method": "PROXY","from": "DOOR","select": "0"}')
                    self.send_params(self.pred_class)
                    self.synthesiser.play("%s番が選択されました" % self.pred_class)
                    self.enable_detect = True
                    self.reset_audio_state()

            except KeyboardInterrupt:
                os.system('clear')
                self.is_exit = True
                break

        self.recorder.exit()

    def detection(self):
        wav = np.fromstring(self.stream.read(
            config.WAVE_CHUNK, exception_on_overflow=False), np.float32)
        wav *= np.hanning(config.WAVE_CHUNK)
        # amplitude spectrum
        amp_spec = np.fft.fft(wav)
        # power spectrum
        power_spec = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in amp_spec]
        # band-pass filter
        power_spec = preprocessing.filtering(power_spec)

        self.audio_state.current_vol = sum(power_spec)
        self.audio_state.total_vol += self.audio_state.current_vol
        self.audio_state.average_vol = \
            self.audio_state.total_vol / self.audio_state.n_sample

        # start/stop recording
        if self.enable_detect:
            if self.is_recording:
                if self.judge_down_edge() or \
                        time.time() - self.record_start_time > 3:
                    self.audio_state.n_down_edge = 0
                    self.is_recording = False
                    self.enable_detect = False
            else:
                if self.judge_up_edge():
                    self.audio_state.n_up_edge = 0
                    self.is_recording = True
                    self.audio_state.border = self.audio_state.average_vol
                    self.record_start_time = time.time()

    def judge_up_edge(self) -> bool:
        judge_border: int = int(config.WAVE_RATE / config.WAVE_CHUNK / 10)

        if self.audio_state.current_vol >= self.audio_state.border:
            self.audio_state.n_up_edge += 1

        return self.audio_state.n_up_edge > judge_border

    def judge_down_edge(self) -> bool:
        judge_border: int = int(config.WAVE_RATE / config.WAVE_CHUNK / 2)

        if self.audio_state.average_vol <= self.audio_state.border:
            self.audio_state.n_down_edge += 1

        return self.audio_state.n_down_edge > judge_border

    def reset_audio_state(self) -> None:
        self.audio_state.total_vol = \
            self.audio_state.average_vol * config.WAVE_AMP_SAMPLES
        self.audio_state.n_sample = config.WAVE_AMP_SAMPLES
        self.audio_state.n_up_edge = 0
        self.past_time = time.time()

    def draw_field(self) -> None:
        self.anal.draw(
            str(int(self.audio_state.average_vol)),
            str(int(self.audio_state.current_vol)),
            str(int(self.audio_state.border)),
            '\033[%dm録音中' % (32 if self.is_recording else 90),
            '\033[%dm認識中' % (32 if not self.enable_detect else 90),
            self.generate_meter(self.audio_state.average_vol, True),
            self.generate_meter(self.audio_state.current_vol, True),
            self.generate_meter(self.audio_state.border),
            self.pred_class,
            self.log_message,
        )

    def update_border(self) -> None:
        while not self.is_exit:
            time.sleep(0.2)

            # update border only when not recording
            if not self.is_recording:
                self.audio_state.border = \
                    pow(10, 1.13) * pow(self.audio_state.average_vol, 0.72)

    def generate_meter(self, volume: float, to_green: bool = False) -> str:
        result: str = ''
        result = '■' * int(volume / 20.0 + 3.0)
        if to_green and \
                self.audio_state.current_vol >= self.audio_state.border:
            result = '\033[94m' + result

        return result

    def predict(self) -> str:
        result: str
        try:
            files: dict = {'wavfile': open(config.RECORD_WAV_PATH, 'rb')}
            res = requests.post(config.ASR_NUMBER_URL, files=files)
            result = res.json()['text']
        except Exception:
            result = message.ERROR_ASR_SERVER_NOT_STARTED

        return result

    def on_message(self, ws_app, received_message):
        self.log_message = message.WS_ON_MESSAGE(received_message)
        self.draw_field()

        if '訪問者確認' in received_message:
            return

        speech_texts: dict = {
            "置き配": "置き配をお願いいたします",
            "置き配確認": "置き配が可能か確認してください。",
            "在宅確認": "在宅確認中です。しばらくお待ちください。",
            "撃退": "今お母さんいないよ",
            "サイレン": "ただいま呼び出し中です。しばらくお待ちください。",
            "OK": "在宅が確認できました。どうぞ、お入りください",
            "NG": "不在のため、今回はお引き取りください",
        }
        if self.pred_class == '4':
            speech_texts['撃退'] = \
                "わたしが神なので、あなた方の信じる神を信じることはできません。ところで私のことを信仰してみませんか？"

        # play終了まで待機
        while True:
            if self.enable_detect:
                break
            time.sleep(0.2)

        res: dict = json.loads(received_message)
        try:
            self.block_detect = True
            self.is_confirm = False
            text = speech_texts[res['message']]

            if res['message'] == "置き配確認":
                self.is_confirm = True
                self.synthesiser.play("置き配が可能な場合は1を")
                self.synthesiser.play("置き配が不可能な場合は2を")
                text = "選択してください"

            self.log_message = message.PLAY_AUDIO_MSG(text)
            self.draw_field()
            self.synthesiser.play(text)

        except Exception as e:
            self.log_message = message.WS_ON_ERROR(received_message)
            self.draw_field()

        self.reset_audio_state()
        self.block_detect = False

    def on_error(self, ws_app, error):
        self.log_message = message.WS_ON_ERROR(error)
        self.draw_field()

    def on_close(self, ws_app):
        self.is_exit = True
        self.log_message = message.WS_ON_CLOSE
        self.draw_field()

    def on_open(self, ws_app):
        self.log_message = message.WS_ON_OPEN
        self.draw_field()
        thread.start_new_thread(self.start, ())

    def send_params(self, class_str: str) -> None:
        if self.is_confirm and class_str != '1' and class_str != '2':
            text = "1か2を選択してください"
            self.synthesiser.play(text)
            self.log_message = text
            return

        params: dict = {
            "method": 'PROXY',
            "from": 'DOOR',
            "select": class_str,
        }
        params_str: str = json.dumps(params)
        self.log_message = message.WS_SEND_MSG(params_str)
        self.ws_app.send(params_str)
        self.draw_field()
