"""
Base class for pipelines
"""

from abc import ABC, abstractmethod

from core.Tools import Tools


class Pipeline(ABC):
    """
    Abstract protocol for build variants
    """
    pipeline_name: str
    stages: list[str]
    instruments: Tools

    def __init__(self, pipeline_name: str):
        self.pipeline_name = pipeline_name
        self.stages = list()

    def preprocess(self) -> None:
        pass

    def assemble(self) -> None:
        pass

    def compile(self) -> None:
        pass

    def link(self) -> None:
        pass

    @abstractmethod
    def all_build_stages(self) -> None:
        pass

    def deploy(self) -> None:
        pass
