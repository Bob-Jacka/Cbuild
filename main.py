"""
CBuild executable file for building C programs and other.

Supports projects only on big C: C, C++, C#
"""

import argparse
import signal
from pathlib import Path
from typing import Final

from core.config.Config import Config_master
from core.pipelines.Pipeline_runner import Pipeline_runner

try:
    from common_py_lib.entities.Formatter import TextAnsiFormatter
    from common_py_lib.filesystem import Filesystem
except ModuleNotFoundError:
    print('Import private local library first')

VERSION: Final[str] = '0.2.3'
CURRENT_DIR: Final[str] = Path().parent.absolute().as_posix()  # path to current dir where script is stored


def configure_arg_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('-p', '--pipeline', help='Use for pipeline in code deploy', required=False)


def handle_critical_error(msg: str):
    TextAnsiFormatter.prRed(msg)
    exit(1)


def signal_handler(sig, frame):
    """
    Handle sig int command
    :param sig: signal
    :param frame: function to execute in case of signal
    :return: None
    """
    print('\n')
    TextAnsiFormatter.prYellow("Out program")
    exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)  # if program goes wrong
    parser = argparse.ArgumentParser(
        prog='CBuild',
        usage='Pass cbuild config and choose your pipeline',
        description='Custom build system for C programs and linux kernel and other and other',
        epilog='Bye')

    configure_arg_parser(parser)
    # args = parser.parse_args(sys.argv)

    config = Config_master(CURRENT_DIR).read_config()
    runner = Pipeline_runner(config)

    while True:
        TextAnsiFormatter.prYellow('Start pipeline cycle')
        runner.app_cycle()
        TextAnsiFormatter.prYellow('Exit from pipeline cycle')
