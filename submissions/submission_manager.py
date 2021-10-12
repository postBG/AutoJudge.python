from subprocess import TimeoutExpired
from threading import Lock
from typing import List

from submissions.abc import AbstractBaseSubmission


class Counter(object):
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        with self.lock:
            self.count += offset


class SubmissionManager(object):
    def __init__(self, submissions: List[AbstractBaseSubmission]):
        self._submissions_dict = {submission.student_id: submission for submission in submissions}

    def compile_all(self, *args, **kwargs):
        error_cnt = Counter()
        compile_procs = {student_id: submission.compile() for student_id, submission in
                         self._submissions_dict.items()}
        for student_id, proc in compile_procs.items():
            out, err = proc.communicate()
            if proc.returncode:
                error_cnt.increment(1)
                print(err)
            self._submissions_dict[student_id].update_compile_results(err)
        print(f"Compile Failure: {error_cnt.count} / {len(self._submissions_dict)}")

    def run_all(self, test_cases):
        for i, test_case in enumerate(test_cases):
            print(f"Start {test_case.test_id}")
            run_procs = {student_id: submission.run(test_case.input) for student_id, submission in
                         self._submissions_dict.items()}
            for student_id, proc in run_procs.items():
                try:
                    out = proc.communicate(timeout=10)[0]
                    score = test_case.get_score(out)
                    self._submissions_dict[student_id].update_score(test_case.test_id, score)
                except TimeoutExpired:
                    self._submissions_dict[student_id].update_score(test_case.test_id, score=0)
                    proc.kill()
