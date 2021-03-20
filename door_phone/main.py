#!/usr/bin/env python3
import argparse

from core import speech_synth


def start_mode():
    synthesiser = speech_synth.SpeechSynth()
    synthesiser.play('今日はいい天気ですね。')


if __name__ == '__main__':
    # options
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start',
                        help='start mode',
                        action='store_true')
    args = parser.parse_args()

    if args.start:
        start_mode()
