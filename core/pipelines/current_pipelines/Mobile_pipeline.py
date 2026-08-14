"""
Pipeline for C# android experience on my phone
"""
import subprocess

from common_py_lib.entities.Formatter import TextAnsiFormatter

from core.Tools import Tools
from core.pipelines.Pipeline import Pipeline

mobile_tools = {
    'compile': 'build -t:SignAndroidPackage -c Release',
    'deploy': 'run -f net8.0-android'
}


class Mobile_pipeline(Pipeline):

    def __init__(self, pipeline_name: str):
        self.instruments = Tools(**mobile_tools)
        super().__init__(pipeline_name)

    def compile(self) -> None:
        op_res = subprocess.run(f'dotnet {self.instruments.compile}').returncode
        if op_res == 0:
            TextAnsiFormatter.prGreen('Successful command execution')
        else:
            TextAnsiFormatter.prRed(f'Mobile compile returned - {op_res}')

    def all_build_stages(self) -> None:
        pass

    def deploy(self) -> None:
        op_res = subprocess.run(f'dotnet {self.instruments.deploy}').returncode
        if op_res == 0:
            TextAnsiFormatter.prGreen('Successful deploy command execution')
        else:
            TextAnsiFormatter.prRed(f'Mobile deploy returned - {op_res}')
