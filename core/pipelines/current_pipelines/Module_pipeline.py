"""
Pipeline for Linux kernel modules
"""
from core.Tools import Tools
from core.pipelines import IPipeline

module_tools = {
    'assemble': 'nasm',  # favourite assembly compiler
    'compile': 'gcc',  # favourite c compiler
    'link': 'ld',  # favourite linker
    'deploy': 'sudo insmod'
}


class Module_pipeline(IPipeline):
    def __init__(self, pipeline_name: str):
        self.instruments = Tools(**module_tools)
        super().__init__(pipeline_name)

    def run_pipeline(self):
        pass

    def preprocess(self) -> None:
        pass

    def assemble(self) -> None:
        pass

    def compile(self) -> None:
        pass

    def link(self) -> None:
        pass

    def all_build_stages(self) -> None:
        pass

    def deploy(self) -> None:
        pass
