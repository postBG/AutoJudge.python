import abc
from collections import defaultdict
from subprocess import Popen


class ResultData(object):
    def __init__(self):
        super().__init__()
        self._compile_results = None
        self._scores = defaultdict(dict)

    def update_compile_result(self, results):
        self._compile_results = results

    def get_compile_results(self):
        return (self._compile_results == b''), self._compile_results

    def add(self, problem_id, test_case_id, score):
        self._scores[problem_id][test_case_id] = score

    def total_score(self, problem_id=None):
        if problem_id:
            return sum(self._scores[problem_id].values())

        total_score = 0
        for problem_id, scores in self._scores.items():
            total_score += sum(scores.values())
        return total_score

    def summary(self):
        result_statistics = {}
        for problem_id, scores in self._scores.items():
            result_statistics[problem_id] = {
                'total_score': self.total_score(problem_id),
                'num_test_cases': len(scores)
            }
        result_statistics['total'] = {
            'total_score': self.total_score(),
            'num_test_cases': self._count_num_tests()
        }
        result_statistics['compile_result'] = self._compile_results
        return result_statistics

    def _count_num_tests(self):
        total_num_tests = 0
        for problem_id, scores in self._scores.items():
            total_num_tests += len(scores)
        return total_num_tests

    def __repr__(self):
        summary = self.summary()
        return f"summary: {summary['total']} ({summary['compile_result']})"


class AbstractBaseSubmission(abc.ABC):
    def __init__(self):
        self._compile_results = None
        self._test_results = ResultData()

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

    def update_compile_results(self, results):
        self._test_results.update_compile_result(results)

    def update_score(self, problem_id, test_case_id, score):
        self._test_results.add(problem_id, test_case_id, score)

    def get_results(self):
        return self._test_results
