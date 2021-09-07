import argparse
import os
from subprocess import Popen, PIPE, STDOUT


def main():
    project_root = "/Users/postbg/IdeaProjects/DataStructureAssignment/Assignment1"
    source_root = f"{project_root}/src"
    compile_path = f"{project_root}/out"
    target_path = "problem1"
    target_name = "Main"
    target_filename = f"{target_name}.java"
    target_file_path = os.path.join(source_root, target_path, target_filename)

    assigment_example_path = "/Users/postbg/PycharmProjects/AutoJudge.python/assigment1"
    inputs_path = f"{assigment_example_path}/inputs"
    answers_path = f"{assigment_example_path}/answers"
    inputs = read_file(inputs_path)
    answers = read_file(answers_path)

    proc = compile_code(target_file_path, compile_path)
    proc.communicate()
    for file_name, args in inputs.items():
        proc = run_code(source_root, compile_path, target_path, target_name, args)
        out = proc.communicate()[0]
        print(f'{file_name} result: {out == answers[file_name]}')


def read_file(inputs_path):
    input_example_files = os.listdir(inputs_path)
    inputs = {}
    for input_example_file in input_example_files:
        with open(os.path.join(inputs_path, input_example_file), 'rb') as f:
            args = f.read().replace(b'\r', b'').lstrip(b'\n')
            inputs[input_example_file] = args
    return inputs


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
