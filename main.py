import os

import hydra
from omegaconf import OmegaConf

from test_cases.file_examples import SimpleFileTestCases
from java_utils import compile_code, run_code


@hydra.main(config_path='configs', config_name='default_setup')
def main(configs):
    OmegaConf.set_struct(configs, False)
    submissions_root = configs.submissions_root
    source_root = os.path.join(submissions_root, configs.source_root)
    production_path = os.path.join(submissions_root, configs.production_root)
    target_path = "problem1"
    target_name = configs.target_entry_class
    target_filename = f"{target_name}.java"
    target_file_path = os.path.join(source_root, target_path, target_filename)

    assigment_testcase_root = configs.assigment_testcase_root
    examples = SimpleFileTestCases(assigment_testcase_root)

    proc = compile_code(target_file_path, production_path)
    proc.communicate()
    for i, example in enumerate(examples):
        proc = run_code(source_root, production_path, target_path, target_name, example.input)
        out = proc.communicate()[0]
        print(f'{i}-th score: {example.get_score(out)}')


if __name__ == '__main__':
    main()