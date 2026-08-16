"""
Base class for pipelines
"""
import os
from abc import ABC, abstractmethod

from core.Tools import Tools


class IPipeline(ABC):
    """
    Abstract protocol for build variants
    """
    pipeline_name: str
    stages: list[str]
    type: str = None
    language: str = None
    instruments: Tools

    def __init__(self, pipeline_name: str):
        self.pipeline_name = pipeline_name
        self.stages = list()

    @staticmethod
    def exec_command(command: str) -> int | None:
        """
        Execute cli command and return status code
        :param command: command to run (str)
        :return: status code or None in case of error
        """
        try:
            return os.system(command)
        except Exception as e:
            print(f'An exception during command execution: {e}')

    def preprocess(self) -> None:
        """
        Especially for C or C++, use preprocessor
        :return: None
        """
        pass

    def assemble(self) -> None:
        """
        Get assemble
        :return: None
        """
        pass

    def compile(self) -> None:
        """
        Compile given sources
        :return: None
        """
        pass

    def link(self) -> None:
        """
        Link object files
        :return: None
        """
        pass

    def clean(self) -> None:
        """
        Delete tmp files
        :return: None
        """
        pass

    @abstractmethod
    def all_build_stages(self) -> None:
        pass

    def deploy(self) -> None:
        pass
