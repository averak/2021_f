#!/usr/bin/env python3
import json
import websocket
import argparse

from core import message


def on_message(ws, message):
    print(message.WS_ON_MESSAGE(message))
    return


def on_error(ws, error):
    print(message.WS_ON_ERROR(message))
    return


def on_close(ws):
    print(message.WS_ON_CLOSE)
    return


def on_open(ws, params):
    json_str: str = json.dumps(params)
    print(message.WS_ON_OPEN(json_str))
    ws.send(json_str)


def start_mode():
    from core import speech_synth

    ws_app = websocket.WebSocketApp(
        config.INTERMEDIATE_SERVER_URL,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open,
    )
    ws_app.run_forever()

    # synthesiser = speech_synth.SpeechSynth()
    # synthesiser.play('音声合成テストです')


if __name__ == '__main__':
    # options
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start',
                        help='start mode',
                        action='store_true')
    args = parser.parse_args()

    if args.start:
        start_mode()
