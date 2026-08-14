from core.Tools import Tools
from core.pipelines.Pipeline import Pipeline

c_tools = {

}


class C_pipeline(Pipeline):
    """
    Pipeline for usual C programs.
    """

    def __init__(self, pipeline_name: str):
        self.instruments = Tools(**c_tools)
        super().__init__(pipeline_name)

    def run_pipeline(self):
        pass

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
