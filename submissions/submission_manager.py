from typing import List

from submissions.abc import AbstractBaseSubmission


class SubmissionManager(object):
    def __init__(self, submissions: List[AbstractBaseSubmission]):
        self._submissions_dict = {submission.student_id: submission for submission in submissions}

    def compile_all(self, problem_idx, *args, **kwargs):
        compile_procs = {student_id: submission.compile(problem_idx) for student_id, submission in
                         self._submissions_dict.items()}
        for student_id, proc in compile_procs.items():
            out, err = proc.communicate()
            if proc.returncode:
                print(err)
            self._submissions_dict[student_id].write_compile_results(err)

    def run_all(self, problem_idx, test_cases):
        for i, test_case in enumerate(test_cases):
            run_procs = {student_id: submission.run(problem_idx, test_case.input) for student_id, submission in
                         self._submissions_dict.items()}
            for student_id, proc in run_procs.items():
                out = proc.communicate()[0]
                score = test_case.get_score(out)
                self._submissions_dict[student_id].write_score(problem_idx, i, score)
