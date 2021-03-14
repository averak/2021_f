#!/usr/bin/env python
import argparse


def train_mode():
    # FIXME
    return


def record_mode():
    # FIXME
    return


def build_mode():
    # FIXME
    return


def start_mode():
    # FIXME
    return


def clear_mode():
    # FIXME
    return


if __name__ == '__main__':
    # options
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('-t', '--train',
                        help='training with teacher data',
                        action='store_true')
    parser.add_argument('-r', '--record',
                        help='voice recording audio for training',
                        action='store_true')
    parser.add_argument('-b', '--build',
                        help='build data for training',
                        action='store_true')
    parser.add_argument('-s', '--start',
                        help='start asr-server',
                        action='store_true')
    parser.add_argument('-c', '--clear',
                        help='clear data',
                        action='store_true')
    args = parser.parse_args()

    if args.train:
        train_mode()
    if args.record:
        record_mode()
    if args.build:
        build_mode()
    if args.start:
        start_mode()
    if args.clear:
        clear_mode()
