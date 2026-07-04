"""
CBuild executable file for building C programs and other
"""

import argparse
import signal
import sys
from typing import Final, Protocol

VERSION: Final[str] = '0.0.2'
APP_NAME: Final[str] = 'CBuild'


class Format:
    """
    Utility class for text formater
    Includes print functions in different colors and underline technology.
    """

    @staticmethod
    def prRed(string: str):
        print("\033[91m {}\033[00m".format(string))

    @staticmethod
    def prGreen(string: str):
        print("\033[92m {}\033[00m".format(string))

    @staticmethod
    def prYellow(string: str):
        print("\033[93m {}\033[00m".format(string))

    @staticmethod
    def prCyan(string: str):
        print("\033[96m {}\033[00m".format(string))

    @staticmethod
    def prUnderline(string: str):
        print("\033[4m {}\033[0m".format(string))


class Pipeline(Protocol):
    """
    Abstract protocol for build variants
    """

    def __init__(self):
        pass

    def preprocess(self) -> None: ...

    def assembly(self) -> None: ...

    def compile(self) -> None: ...

    def link(self) -> None: ...

    def all_build_stages(self) -> None: ...

    def deploy(self) -> None: ...


class C_pipeline:
    """
    Pipeline for usual C programs.
    """

    def preprocess(self) -> None:
        pass

    def assembly(self) -> None:
        pass

    def compile(self) -> None:
        pass

    def link(self) -> None:
        pass

    def all_build_stages(self) -> None:
        pass

    def deploy(self) -> None:
        pass


class Embedded_pipeline:
    """
    Pipeline for embedded devices, such as ESP32 or ESP8266.
    Deploy on microcontroller
    """

    def preprocess(self) -> None:
        pass

    def assembly(self) -> None:
        pass

    def compile(self) -> None:
        pass

    def link(self) -> None:
        pass

    def all_build_stages(self) -> None:
        pass

    def deploy(self) -> None:
        pass


class Kernel_pipeline:
    """
    Pipeline for building linux kernel and deploy it on emulator
    """

    def preprocess(self) -> None:
        pass

    def assembly(self) -> None:
        pass

    def compile(self) -> None:
        pass

    def link(self) -> None:
        pass

    def all_build_stages(self) -> None:
        pass

    def deploy(self) -> None:
        pass


class Pipeline_runner:

    def __init__(self):
        pass
        # self.pipeline = #TODO instantiate concrete pipeline

    def app_cycle(self):
        if sys.platform == 'linux':  # only linux is allowed, who will use windows to install another kernel
            print('Used allowed system')
            while True:
                print('Choose option:')
                print('1. Compile assembler')
                print('2. Compile C code')
                print('3. Link entities')
                print('4. Rebuild all stages')  # all stages include

                # run kernel in emulator
                print('5. Run kernel')

                # other:
                print('6. Clear all compiled files')
                print('7. Exit from utility')

                user_input = int(input('>> '))
                match user_input:
                    case 1:
                        self.pipeline.build_asm()
                        continue

                    case 2:
                        self.pipeline.build_c()
                        continue

                    case 3:
                        self.pipeline.use_linker()
                        continue

                    case 4:
                        self.pipeline.all_build_stages()
                        continue

                    case 5:
                        self.pipeline.run_kernel()
                        continue

                    case 6:
                        self.pipeline.clear_dir()
                        continue

                    case 7:
                        print('Exit from kernel build system')
                        exit(0)

                    case _:
                        print('Wrong option, try again')
                        continue
        else:
            print(f'Your system is not allowed - {sys.platform}')


def configure_arg_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('-f', '--file', help='Use for start file in pipeline', required=True)
    parser.add_argument('-p', '--pipeline', help='Use for pipeline in code deploy', required=False)


def handle_critical_error(msg: str):
    Format.prRed(msg)
    exit(1)


def signal_handler(sig, frame):
    """
    Handle sig int command
    :param sig: signal
    :param frame: function to execute in case of signal
    :return: None
    """
    print('\n')
    Format.prYellow("Out program")
    exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)  # if program goes wrong
    parser = argparse.ArgumentParser(
        prog=APP_NAME,
        description='Custom build system for C programs and linux kernel',
        epilog='Bye')

    configure_arg_parser(parser)
    args = parser.parse_args(sys.argv)
    Pipeline_runner().app_cycle()
