#!/usr/bin/env python
import argparse

from core import config
from core import message
from core import record
from core import util


def train_mode():
    # FIXME
    return


def record_mode():
    default_source: str = '1'
    input_str: str = input(message.SOURCE_INPUT_GUIDE(default_source)) \
        or default_source

    # set save path
    save_root_path: str = ''
    if input_str == 'noise':
        save_root_path = config.NOISE_ROOT_PATH
    else:
        save_root_path = config.SPEECH_ROOT_PATH + '/' + input_str

    # mkdir & count number of exists files
    util.mkdir(save_root_path)
    save_index: int = util.get_number_of_files(save_root_path, 'wav')

    recorder: record.Record = record.Record()
    start_recording: bool = True

    print(message.RECORDING_HELP_MSG)
    while input() != 'q':
        if start_recording:
            recorder.start()
            print(message.RECORDING_VOICE_MSG(save_index), end='')
        else:
            recorder.stop()

            # <save_root_path>/<save_index>.wav
            file_name: str = '%s/%d.wav' % (save_root_path, save_index)
            recorder.save(file_name)
            print(message.CREATED_FILE_MSG(file_name))
            save_index += 1

        start_recording = not start_recording

    print(message.CREATED_DATA_MSG(save_index))
    recorder.exit()


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
