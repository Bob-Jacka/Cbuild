import dataclasses
import os
import re

from core.pipelines.IPipeline import IPipeline


@dataclasses.dataclass
class Config:
    config_name: str
    pipelines: list[IPipeline]  # pipeline to run

    def __init__(self, config_name: str, pipeline_list: list[IPipeline]):
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
        self.config: str = configs[0]

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
        pipelines: list[IPipeline] = list()
        with open(self.config) as config:
            config_name = self.config.removesuffix('.cbuild')
            config_data = config.readlines()

            for line in config_data:
                line = line.strip()

                if not line or line.startswith("#") or line.startswith('{') or line.startswith('}'):  # comment line
                    continue

                if line.startswith('Type'):
                    if not match:
                        print('Cannot read pipeline type')
                        continue
                    pipeline.type = re.match(r'Type\s+([^"]+)', line).group(1)
                    continue

                if line.startswith('Language'):
                    match = re.match(r'Language\s+([^"]+)', line)
                    if not match:
                        print('Cannot read pipeline language')
                        continue
                    pipeline.language = match.group(1)
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
