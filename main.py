import os
from subprocess import Popen, PIPE

import hydra
from omegaconf import OmegaConf

from examples.file_examples import read_file, SimpleFileExamples


@hydra.main(config_path='configs', config_name='default_setup')
def main(configs):
    OmegaConf.set_struct(configs, False)
    project_root = configs.project_root
    source_root = os.path.join(project_root, configs.source_root)
    production_path = os.path.join(project_root, configs.production_root)
    target_path = "problem1"
    target_name = configs.target_entry_class
    target_filename = f"{target_name}.java"
    target_file_path = os.path.join(source_root, target_path, target_filename)

    assigment_examples_root = configs.assigment_examples_root
    examples = SimpleFileExamples(assigment_examples_root)

    proc = compile_code(target_file_path, production_path)
    proc.communicate()
    for i, example in enumerate(examples):
        proc = run_code(source_root, production_path, target_path, target_name, example.input)
        out = proc.communicate()[0]
        print(f'{i}-th score: {example.get_score(out)}')


def compile_code(file_path, compile_path):
    proc = Popen(['javac', '-d', compile_path, file_path])
    return proc


def run_code(project_path, compile_path, target_path, target_name, inputs):
    classpath = os.path.join(project_path, compile_path)
    target_class = '.'.join([target_path, target_name])
    proc = Popen(['java', '-classpath', classpath, target_class], stdin=PIPE, stdout=PIPE)
    proc.stdin.write(inputs)
    return proc


if __name__ == '__main__':
    main()
