"""
CBuild executable file for building C programs
"""
import argparse
from typing import Final

VERSION: Final[str] = '0.0.1'


def configure_arg_parser(parser: argparse.ArgumentParser):
    parser.add_argument('-h', '--help', help='just help flag')
    parser.add_argument('-f', '--file', help='Use for start file in pipeline')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='CBuild',
        description='Custom build system for C programs and linux kernel',
        epilog='Bye')

    configure_arg_parser(parser)
