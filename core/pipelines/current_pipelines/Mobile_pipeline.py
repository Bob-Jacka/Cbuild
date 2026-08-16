"""
Pipeline for C# android experience on my phone
"""

from common_py_lib.entities.Formatter import TextAnsiFormatter

from core.Tools import Tools
from core.pipelines.IPipeline import IPipeline

mobile_tools = {
    'compile': 'build -t:SignAndroidPackage -c Release',
    'deploy': 'run -f net8.0-android'
}


class Mobile_pipeline(IPipeline):

    def __init__(self, pipeline_name: str):
        self.instruments = Tools(**mobile_tools)
        super().__init__(pipeline_name)

    def check_device(self):
        op_res = IPipeline.exec_command('adb devices')
        if op_res == 0:
            TextAnsiFormatter.prGreen('Device is connected')
        else:
            raise Exception('Device is not connected')

    def compile(self) -> None:
        op_res = IPipeline.exec_command(f'dotnet {self.instruments.compile}')
        if op_res == 0:
            TextAnsiFormatter.prGreen('Successful command execution')
        else:
            TextAnsiFormatter.prRed(f'Mobile compile returned - {op_res}')

    def all_build_stages(self) -> None:
        pass

    def deploy(self) -> None:
        self.check_device()
        op_res = IPipeline.exec_command(f'dotnet {self.instruments.deploy}')
        if op_res == 0:
            TextAnsiFormatter.prGreen('Successful deploy command execution')
        else:
            TextAnsiFormatter.prRed(f'Mobile deploy returned - {op_res}')
