import os
from subprocess import Popen, PIPE

from submissions.abc import AbstractBaseSubmission
from submissions.utils import extract_student_id_from

SOURCE_ROOT = "src"
PRODUCTION_ROOT = "snu_out"
TARGET_CLASS_NAME = "Main"


class JavaSubmission(AbstractBaseSubmission):
    def __init__(self, project_root):
        super().__init__()
        self._student_id = extract_student_id_from(project_root)
        self._project_root = project_root
        self._source_root = os.path.join(project_root, SOURCE_ROOT)
        self._production_root = os.path.join(project_root, PRODUCTION_ROOT)

    def compile(self, problem_id, *args, **kwargs) -> Popen:
        compile_target = os.path.join(self._source_root, '**', "*.java")
        proc = Popen(['javac', '-cp . -d', self._production_root, compile_target], stdout=PIPE, stderr=PIPE)
        return proc

    def run(self, problem_id, inputs, *args, **kwargs) -> Popen:
        classpath = self._production_root
        proc = Popen(['java', '-classpath', classpath, TARGET_CLASS_NAME], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        proc.stdin.write(inputs)
        return proc

    @property
    def student_id(self):
        return self._student_id
