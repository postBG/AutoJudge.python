from subprocess import TimeoutExpired
from threading import Lock
from typing import List

from submissions.abc import AbstractBaseSubmission


class CompileResult(object):
    def __init__(self):
        self.lock = Lock()
        self.failed_students = []

    def increment(self, student_id):
        with self.lock:
            self.failed_students.append(student_id)

    def __len__(self):
        return len(self.failed_students)


class SubmissionManager(object):
    def __init__(self, submissions: List[AbstractBaseSubmission]):
        self._submissions_dict = {submission.student_id: submission for submission in submissions}

    def compile_all(self, *args, **kwargs):
        result = CompileResult()
        compile_procs = {student_id: submission.compile() for student_id, submission in
                         self._submissions_dict.items()}
        for student_id, proc in compile_procs.items():
            out, err = proc.communicate()
            if proc.returncode:
                result.increment(student_id)
                print(err)
            self._submissions_dict[student_id].update_compile_results(err)
        return result

    def run_all(self, test_cases, timeout=10):
        for i, test_case in enumerate(test_cases):
            print(f"Start {test_case.test_id}")
            run_procs = {student_id: submission.run(test_case.input) for student_id, submission in
                         self._submissions_dict.items()}
            for student_id, proc in run_procs.items():
                try:
                    out = proc.communicate(timeout=timeout)[0]
                    score = test_case.get_score(out)
                    self._submissions_dict[student_id].update_score(test_case.test_id, score)
                    self._submissions_dict[student_id].update_output(test_case.test_id, out)
                except TimeoutExpired:
                    self._submissions_dict[student_id].update_score(test_case.test_id, score=0)
                    self._submissions_dict[student_id].update_output(test_case.test_id, "Time Expired!")
                    proc.kill()
