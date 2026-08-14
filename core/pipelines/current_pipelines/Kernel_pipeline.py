import subprocess

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
    'deploy': 'qemu'
}


class Kernel_pipeline(Pipeline):
    """
    Pipeline for building linux kernel and deploy it on emulator
    """

    def __init__(self, pipeline_name: str):
        self.instruments = Tools(**kernel_tools)
        super().__init__(pipeline_name)

    def assembly(self) -> None:
        # nasm -f elf32 start_point.asm -o kasm.o
        TextAnsiFormatter.prYellow('Compiling assembler code')
        if Path_master.current_dir_files.__contains__('start_point.asm'):
            op_res = subprocess.run(f'{self.instruments.assemble} -f elf32 start_point.asm -o kasm.o').returncode
            if op_res == 0:
                print('Successful command execution')
            else:
                TextAnsiFormatter.prRed(f'Not successful command - {op_res} code')
            return
        else:
            TextAnsiFormatter.prRed('Current directory not contains asm file')

    def compile(self) -> None:
        # gcc -m32 -c main.c -o kc.o
        TextAnsiFormatter.prYellow('Compiling "C" code')
        if Path_master.current_dir_files.__contains__('main.c'):
            op_res = subprocess.run(f'{self.instruments.compile} -m32 -c main.c -o kc.o').returncode
            if op_res == 0:
                print('Successful command execution')
            else:
                TextAnsiFormatter.prRed(f'Not successful command - {op_res} code')
            return
        else:
            TextAnsiFormatter.prRed('Current directory not contains main.c file')

    def link(self) -> None:
        # ld -m elf_i386 -T link.ld -o kernel kasm.o kc.o
        TextAnsiFormatter.prYellow('Using linking')
        if Path_master.current_dir_files.__contains__('main.c') and Path_master.current_dir_files.__contains__('start_point.asm'):
            f'{self.instruments.assemble} -f elf32 start_point.asm -o kasm.o'
            op_res = subprocess.run(f'{self.instruments.link} -m elf_i386 -T link.ld -o kernel kasm.o kc.o').returncode
            if op_res == 0:
                TextAnsiFormatter.prGreen('Successful command execution')
            else:
                TextAnsiFormatter.prRed(f'Not successful command - {op_res} code')
                TextAnsiFormatter.prYellow('Try with stack protector')

                # gcc -fno-stack-protector -m32 -c main.c -o kc.o
                another_try = subprocess.run(f'{self.instruments.compile} -fno-stack-protector -m32 -c main.c -o kc.o')
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
        subprocess.run(f'{self.instruments.deploy} kernel')
