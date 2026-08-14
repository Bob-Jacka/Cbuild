import dataclasses
import os
import re

from core.pipelines.Pipeline import Pipeline


@dataclasses.dataclass
class Config:
    config_name: str
    pipelines: list[Pipeline]  # pipeline to run

    def __init__(self, config_name: str, pipeline_list: list[Pipeline]):
        self.config_name = config_name
        self.pipelines = pipeline_list


class Config_master:
    """
    Read config file of the pipeline
    """

    def __init__(self, start_path: str):
        configs = list(filter(lambda x: x.endswith('.cbuild'), os.listdir(start_path)))
        if len(configs) > 1:
            print('Several configs, this functionality is not implemented')
        elif len(configs) == 0:
            raise Exception('No config found in directory, provide one or go away')
        self.config = configs[0]

    def read_config(self) -> Config:
        """
        Read config for pipelines and stages
        :return: created config file with all data
        """
        from core.pipelines.current_pipelines.Kernel_pipeline import Kernel_pipeline
        from core.pipelines.current_pipelines.C_pipeline import C_pipeline
        from core.pipelines.current_pipelines.Embedded_pipeline import Embedded_pipeline
        from core.pipelines.current_pipelines.Mobile_pipeline import Mobile_pipeline
        config_name: str
        pipelines: list[Pipeline] = list()
        with open(self.config) as config:
            config_name = self.config
            config_data = config.readlines()

            for line in config_data:
                line = line.strip()
                if not line or line.startswith("#") or line.startswith('{') or line.startswith('}'):  # comment line
                    continue

                if line.startswith("Pipeline "):
                    match = re.match(r'Pipeline\s+"([^"]+)"', line)
                    if not match:
                        continue
                    current_pipeline_name = match.group(1)
                    match current_pipeline_name:
                        case 'kernel':
                            pipeline = Kernel_pipeline(current_pipeline_name)
                        case 'embedd':
                            pipeline = Embedded_pipeline(current_pipeline_name)
                        case 'mobile':
                            pipeline = Mobile_pipeline(current_pipeline_name)
                        case 'c':
                            pipeline = C_pipeline(current_pipeline_name)
                    continue

                if line.startswith("Stage: "):
                    if pipeline is None:
                        raise ValueError(f"Stage out of Pipeline block: {line}")
                    match = re.match(r'Stage:\s*"([^"]+)"', line)
                    if not match:
                        raise ValueError(f"Unknown Stage format: {line}")
                    pipeline.stages.append(match.group(1))
                    continue
                else:
                    raise Exception('No pipeline name is specified')

            pipelines.append(pipeline)

        return Config(config_name, pipelines)
