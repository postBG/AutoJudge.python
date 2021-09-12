import os
from subprocess import Popen, PIPE

from submissions.abc import AbstractBaseSubmission
from submissions.utils import extract_student_id_from

SOURCE_ROOT = "src"
PRODUCTION_ROOT = "snu_out"
TARGET_CLASS_NAME = "Main"


def compile_code(file_path, compile_path):
    proc = Popen(['javac', '-d', compile_path, file_path])
    return proc


def run_code(project_path, compile_path, target_path, target_name, inputs):
    classpath = os.path.join(project_path, compile_path)
    target_class = '.'.join([target_path, target_name])
    proc = Popen(['java', '-classpath', classpath, target_class], stdin=PIPE, stdout=PIPE)
    proc.stdin.write(inputs)
    return proc


class JavaSubmission(AbstractBaseSubmission):
    def __init__(self, project_root):
        super().__init__()
        self._student_id = extract_student_id_from(project_root)
        self._project_root = project_root
        self._source_root = os.path.join(project_root, SOURCE_ROOT)
        self._production_root = os.path.join(project_root, PRODUCTION_ROOT)

    def compile(self, problem_id, *args, **kwargs) -> Popen:
        target_package = self._target_package(problem_id)
        compile_target = os.path.join(self._source_root, target_package, f"{TARGET_CLASS_NAME}.java")
        proc = Popen(['javac', '-d', self._production_root, compile_target])
        return proc

    def run(self, problem_id, inputs, *args, **kwargs) -> Popen:
        target_package = self._target_package(problem_id)
        classpath = self._production_root
        target_class = '.'.join([target_package, TARGET_CLASS_NAME])
        proc = Popen(['java', '-classpath', classpath, target_class], stdin=PIPE, stdout=PIPE)
        proc.stdin.write(inputs)
        return proc

    @property
    def student_id(self):
        return self._student_id

    @staticmethod
    def _target_package(problem_id):
        return f"problem{problem_id + 1}"
