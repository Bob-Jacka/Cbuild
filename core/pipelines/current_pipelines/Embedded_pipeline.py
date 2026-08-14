from core.Tools import Tools
from core.pipelines.Pipeline import Pipeline

embedded_tools = {

}

class Embedded_pipeline(Pipeline):
    """
    Pipeline for embedded devices, such as ESP32 or ESP8266.
    Deploy on microcontroller
    """

    def __init__(self, pipeline_name: str):
        self.instruments = Tools(**embedded_tools)
        super().__init__(pipeline_name)

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