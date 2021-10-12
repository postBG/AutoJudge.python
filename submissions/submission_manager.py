from typing import List

from submissions.abc import AbstractBaseSubmission


class SubmissionManager(object):
    def __init__(self, submissions: List[AbstractBaseSubmission]):
        self._submissions_dict = {submission.student_id: submission for submission in submissions}

    def compile_all(self, *args, **kwargs):
        compile_procs = {student_id: submission.compile() for student_id, submission in
                         self._submissions_dict.items()}
        for student_id, proc in compile_procs.items():
            out, err = proc.communicate()
            if proc.returncode:
                print(err)
            self._submissions_dict[student_id].update_compile_results(err)

    def run_all(self, test_cases):
        for i, test_case in enumerate(test_cases):
            run_procs = {student_id: submission.run(test_case.input) for student_id, submission in
                         self._submissions_dict.items()}
            for student_id, proc in run_procs.items():
                out = proc.communicate()[0]
                score = test_case.get_score(out)
                self._submissions_dict[student_id].update_score(test_case.test_id, score)
