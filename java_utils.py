import os
from subprocess import Popen, PIPE


def compile_code(file_path, compile_path):
    proc = Popen(['javac', '-d', compile_path, file_path])
    return proc


def run_code(project_path, compile_path, target_path, target_name, inputs):
    classpath = os.path.join(project_path, compile_path)
    target_class = '.'.join([target_path, target_name])
    proc = Popen(['java', '-classpath', classpath, target_class], stdin=PIPE, stdout=PIPE)
    proc.stdin.write(inputs)
    return proc
