import os
import re
import json
import wave
import pyaudio
import requests

from core import config
from core import message


class SpeechSynth:
    def __init__(self):
        return

    def play(self, text: str) -> None:
        # fetch wav
        if not self.exist_speech(text):
            self.get_text_wav(text)

        # read wav file
        wav = wave.open(self.file_name(text), 'rb')
        # create pyaudio streamer
        pa = pyaudio.PyAudio()
        streamer = pa.open(
            format=pa.get_format_from_width(wav.getsampwidth()),
            channels=wav.getnchannels(),
            rate=wav.getframerate(),
            input=False,
            output=True,
        )
        # play!
        print(message.PLAY_AUDIO_MSG(text))
        voice = wav.readframes(config.WAVE_CHUNK)
        while len(voice) > 0:
            streamer.write(voice)
            voice = wav.readframes(config.WAVE_CHUNK)
        wav.close()
        streamer.stop_stream()
        streamer.close()
        pa.terminate()

    def get_text_wav(self, text: str) -> None:
        """ textを音声に変換します """

        APIKEY = os.environ['DOCOMO_TOKEN']
        url: str = config.DOCOMO_URL + APIKEY
        params: dict = {
            "Command": config.DOCOMO_COMMAND,
            "SpeakerID": config.DOCOMO_SPEAKER_ID,
            "StyleID": config.DOCOMO_STYLE_ID,
            "SpeechRate": config.DOCOMO_SPEECH_RATE,
            "AudioFileFormat": config.DOCOMO_AUDIO_FILE_FORMAT,
            "TextData": text
        }

        # send post
        res = requests.post(
            url,
            data=json.dumps(params),
            headers={'content-type': 'application/json'},
        )

        # dump!
        wav = res.content
        with open(self.file_name(text), 'wb') as f:
            f.write(wav)
        print(message.CREATED_FILE_MSG(self.file_name(text)))

    def file_name(self, text: str) -> str:
        text = re.sub(r"[。．、，,.]", "", text)
        return "%s/%s.wav" % (config.DATA_ROOT_PATH, text)

    def exist_speech(self, text: str) -> bool:
        return os.path.isfile(self.file_name(text))
