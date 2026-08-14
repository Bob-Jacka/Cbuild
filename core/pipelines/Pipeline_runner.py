import sys

from common_py_lib.io.Input import int_input_from_user

try:
    from common_py_lib.entities.Formatter import TextAnsiFormatter
    from common_py_lib.actions.Input import check_infinity_int_input
    from common_py_lib.filesystem.Filesystem import CLOSE_MENU_CODE
except ModuleNotFoundError:
    print('Import private local library first')


class Pipeline_runner:

    def __init__(self, config):
        pipelines_count = len(config.pipelines)
        if pipelines_count > 1:
            TextAnsiFormatter.prYellow('Found several available pipelines in directory:')
            for num, pipeline in enumerate(config.pipelines):
                print(f'{num}: {pipeline.pipeline_name}')

            active_pipeline_num = check_infinity_int_input(pipelines_count, 'Pick one pipeline by its name to run:')
            self.active_pipeline = config.pipelines[active_pipeline_num]
        else:
            self.active_pipeline = config.pipelines[0]

    def app_cycle(self):
        if sys.platform == 'linux':  # only linux is allowed, who will use windows to install another kernel
            TextAnsiFormatter.prYellow('Used allowed system')
            TextAnsiFormatter.prYellow('Use only allowed actions')
            stage_count = len(self.active_pipeline.stages)
            while True:
                print()  # just new line
                TextAnsiFormatter.prYellow(f'Active pipeline name: {self.active_pipeline.pipeline_name}')
                TextAnsiFormatter.prYellow('Choose option:')
                for num, option in enumerate(self.active_pipeline.stages):
                    print(f'{num}: {option.lower()}')
                print(f'{stage_count}: All build stages')  # last, but not least - all stages run
                print(f'{CLOSE_MENU_CODE}. Exit from pipeline runner')

                user_input = int_input_from_user(stage_count, 'Enter pipeline action')
                if user_input == stage_count:
                    self.active_pipeline.all_build_stages()
                    continue
                if user_input == CLOSE_MENU_CODE:
                    print(f'Exit from {self.active_pipeline.pipeline_name} build system')
                    break

                function = getattr(self.active_pipeline, self.active_pipeline.stages[user_input].lower())
                function()

        else:
            print(f'Your system is not allowed - {sys.platform}')
            raise NotImplementedError('System is not allowed for use in CBuild')
