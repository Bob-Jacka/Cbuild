"""
CBuild executable file for building C programs and other
"""

import argparse
import os
import signal
import sys
from pathlib import Path
from typing import Final, Protocol


class Consts:
    VERSION: Final[str] = '0.0.3'
    APP_NAME: Final[str] = 'CBuild'

    # default entities:
    ASSEMBLY_COMPILER: Final[str] = 'nasm'  # favourite assembly compiler
    C_COMPILER: Final[str] = 'gcc'  # favourite c compiler
    LINKER: Final[str] = 'ld'  # favourite linker

    CURRENT_DIR: Final[str] = Path().parent.absolute()  # path to current dir where script is stored


class Path_master:

    def __init__(self):
        if os.listdir(Consts.CURRENT_DIR):
            pass

    current_dir_files: list[str] = list(
        filter(lambda x: not x.startswith('.') or x.endswith('.c') or x.endswith('.asm') or x.endswith('.ld'),
               os.listdir(Consts.CURRENT_DIR))
    )
    """
    Only visible files in directory that fit protocol 
    """

    def create_build_files_dir(self):
        pass

    def delete_build_files(self):
        pass


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

    def all_build_stages(self) -> None: ...  # same as rebuild

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
        # nasm -f elf32 start_point.asm -o kasm.o
        Format.prYellow('Compiling assembler code')
        if Path_master.current_dir_files.__contains__('start_point.asm'):
            op_res = os.system(f'{Consts.ASSEMBLY_COMPILER} -f elf32 start_point.asm -o kasm.o')
            if op_res == 0:
                print('Successful command execution')
            else:
                Format.prRed(f'Not successful command - {op_res} code')
            return
        else:
            Format.prRed('Current directory not contains asm file')

    def compile(self) -> None:
        # gcc -m32 -c main.c -o kc.o
        Format.prYellow('Compiling "C" code')
        if Path_master.current_dir_files.__contains__('main.c'):
            op_res = os.system(f'{Consts.C_COMPILER} -m32 -c main.c -o kc.o')
            if op_res == 0:
                print('Successful command execution')
            else:
                Format.prRed(f'Not successful command - {op_res} code')
            return
        else:
            Format.prRed('Current directory not contains main.c file')

    def link(self) -> None:
        # ld -m elf_i386 -T link.ld -o kernel kasm.o kc.o
        Format.prYellow('Using linking')
        if Path_master.current_dir_files.__contains__('main.c') and Path_master.current_dir_files.__contains__('start_point.asm'):
            op_res = os.system(f'{Consts.LINKER} -m elf_i386 -T link.ld -o kernel kasm.o kc.o')
            if op_res == 0:
                Format.prGreen('Successful command execution')
            else:
                Format.prRed(f'Not successful command - {op_res} code')
                Format.prYellow('Try with stack protector')

                # gcc -fno-stack-protector -m32 -c main.c -o kc.o
                another_try = os.system(f'{Consts.C_COMPILER} -fno-stack-protector -m32 -c main.c -o kc.o')
                self.link()  # another try of linker usage
                if another_try == 0:
                    Format.prGreen('Success retry')
                else:
                    Format.prRed('Still error')
            return
        else:
            Format.prRed('Current directory not contains any of compiled files')

    def all_build_stages(self) -> None:
        pass

    def deploy(self) -> None:
        pass


class Pipeline_runner:
    pipeline: Pipeline  # pipeline to run
    path_wizard: Path_master  # for path actions

    def __init__(self, arguments: list[str] = None):
        if arguments is None:
            pass
        else:
            pass

    def app_cycle(self):
        if sys.platform == 'linux':  # only linux is allowed, who will use windows to install another kernel
            print('Used allowed system')
            while True:
                print('Choose option:')
                print('0. Only preprocess files')
                print('1. Compile assembler')
                print('2. Compile code')
                print('3. Link entities')
                print('4. Rebuild all stages')  # all stages include

                # run kernel in qemu emulator
                print('5. Deploy code')

                # other:
                print('6. Clear all compiled files')
                print('7. Exit from utility')

                user_input = int(input('>> '))
                if user_input in range(8):
                    match user_input:
                        case 0:
                            pass
                        case 1:
                            self.pipeline.assembly()
                            continue

                        case 2:
                            self.pipeline.compile()
                            continue

                        case 3:
                            self.pipeline.link()
                            continue

                        case 4:
                            self.pipeline.all_build_stages()
                            continue

                        case 5:
                            self.pipeline.deploy()
                            continue

                        case 6:
                            self.path_wizard.delete_build_files()
                            continue

                        case 7:
                            print('Exit from kernel build system')
                            exit(0)
                else:
                    print('Wrong option, try again')
                    continue

        else:
            print(f'Your system is not allowed - {sys.platform}')


def configure_arg_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('-f', '--file', action='append', type=str, help='Use for start file in pipeline', required=True)
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
        prog=Consts.APP_NAME,
        usage='Pass start file and optionally choose your pipeline',
        description='Custom build system for C programs and linux kernel',
        epilog='Bye')

    configure_arg_parser(parser)
    args = parser.parse_args(sys.argv)
    if args.file:
        print(f"File: {args.file}")

    runner = Pipeline_runner()
    runner.app_cycle()
