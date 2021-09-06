import argparse
import os
from subprocess import Popen, PIPE, STDOUT


def main():
    project_root = "/Users/postbg/IdeaProjects/JavaTest"
    source_root = f"{project_root}/src"
    compile_path = f"{project_root}/out"
    target_path = "problem1"
    target_name = "Main"
    target_filename = f"{target_name}.java"
    target_file_path = os.path.join(source_root, target_path, target_filename)

    proc = compile_code(target_file_path, compile_path)
    proc.communicate()
    proc = run_code(source_root, compile_path, target_path, target_name)
    out = proc.communicate()[0]
    print(out == b'5\n')


def compile_code(file_path, compile_path):
    proc = Popen(['javac', '-d', compile_path, file_path])
    return proc


def run_code(project_path, compile_path, target_path, target_name):
    classpath = os.path.join(project_path, compile_path)
    target_class = '.'.join([target_path, target_name])
    proc = Popen(['java', '-classpath', classpath, target_class], stdin=PIPE, stdout=PIPE)
    proc.stdin.write(b'5')
    return proc


if __name__ == '__main__':
    main()
