import abc
from collections import defaultdict
from subprocess import Popen


class AbstractBaseSubmission(abc.ABC):
    def __init__(self):
        self._compile_results = None
        self._scores = defaultdict(dict)

    @property
    @abc.abstractmethod
    def student_id(self):
        raise NotImplementedError

    @abc.abstractmethod
    def compile(self, *args, **kwargs) -> Popen:
        raise NotImplementedError

    @abc.abstractmethod
    def run(self, problem_id, inputs, *args, **kwargs) -> Popen:
        raise NotImplementedError

    def write_compile_results(self, results):
        self._compile_results = results

    def get_compile_results(self):
        """return True if compiled successfully along with compile_results itself"""
        return (self._compile_results == b''), self._compile_results

    def write_score(self, problem_id, test_case_id, score):
        self._scores[problem_id][test_case_id] = score

    def get_test_summary(self):
        """return total_score with scores itself"""
        total_score = 0
        for problem_id, scores in self._scores.items():
            total_score += sum(scores.values())
        return total_score, self._scores
