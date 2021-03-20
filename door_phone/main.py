#!/usr/bin/env python3
import argparse


def start_mode():
    from core import speech_synth

    synthesiser = speech_synth.SpeechSynth()
    synthesiser.play('音声合成テストです')


def demo_mode():
    from core import demo

    demo_ = demo.Demo()
    demo_.exec()


if __name__ == '__main__':
    # options
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start',
                        help='start mode',
                        action='store_true')
    parser.add_argument('-d', '--demo',
                        help='demo mode',
                        action='store_true')
    args = parser.parse_args()

    if args.start:
        start_mode()
    if args.demo:
        demo_mode()
