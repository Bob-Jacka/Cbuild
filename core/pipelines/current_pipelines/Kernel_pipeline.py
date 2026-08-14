import os

from core.Path_master import check_for_file
from core.Tools import Tools
from core.pipelines.Pipeline import Pipeline

try:
    from common_py_lib.entities.Formatter import TextAnsiFormatter
except ModuleNotFoundError:
    print('Import private local library first')

kernel_tools = {
    'assemble': 'nasm',  # favourite assembly compiler
    'compile': 'gcc',  # favourite c compiler
    'link': 'ld',  # favourite linker
    'deploy': 'qemu-system-i386 -kernel'
}


class Kernel_pipeline(Pipeline):
    """
    Pipeline for building linux kernel and deploy it on emulator
    """

    def __init__(self, pipeline_name: str):
        self.instruments = Tools(**kernel_tools)
        super().__init__(pipeline_name)

    def assemble(self) -> None:
        # nasm -f elf32 start_point.asm -o kasm.o
        TextAnsiFormatter.prYellow('Compiling assembler code')
        if check_for_file('start_point.asm'):
            op_res = os.system(f'{self.instruments.assemble} -f elf32 start_point.asm -o kasm.o')
            if op_res == 0:
                TextAnsiFormatter.prGreen('Successful command execution')
            else:
                TextAnsiFormatter.prRed(f'Not successful command - {op_res} code')
            return
        else:
            TextAnsiFormatter.prRed('Current directory not contains asm file')

    def compile(self) -> None:
        # gcc -m32 -c main.c -o kc.o
        TextAnsiFormatter.prYellow('Compiling "C" code')
        if check_for_file('main.c'):
            op_res = os.system(f'{self.instruments.compile} -m32 -c main.c -o kc.o')
            if op_res == 0:
                TextAnsiFormatter.prGreen('Successful command execution')
            else:
                TextAnsiFormatter.prRed(f'Not successful command - {op_res} code')
            return
        else:
            TextAnsiFormatter.prRed('Current directory not contains main.c file')

    def link(self) -> None:
        # ld -m elf_i386 -T link.ld -o kernel kasm.o kc.o
        TextAnsiFormatter.prYellow('Using linking')
        if check_for_file('main.c') and check_for_file('start_point.asm'):
            f'{self.instruments.assemble} -f elf32 start_point.asm -o kasm.o'
            op_res = os.system(f'{self.instruments.link} -m elf_i386 -T link.ld -o kernel kasm.o kc.o')
            if op_res == 0:
                TextAnsiFormatter.prGreen('Successful command execution')
            else:
                TextAnsiFormatter.prRed(f'Not successful command - {op_res} code')
                TextAnsiFormatter.prYellow('Try with stack protector')

                # gcc -fno-stack-protector -m32 -c main.c -o kc.o
                another_try = os.system(f'{self.instruments.compile} -fno-stack-protector -m32 -c main.c -o kc.o')
                self.link()  # another try of linker usage
                if another_try == 0:
                    TextAnsiFormatter.prGreen('Success retry')
                else:
                    TextAnsiFormatter.prRed('Still error')
            return
        else:
            TextAnsiFormatter.prRed('Current directory not contains any of compiled files')

    def all_build_stages(self) -> None:
        pass

    def deploy(self) -> None:
        os.system(f'{self.instruments.deploy} kernel')
