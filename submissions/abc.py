import abc
from collections import defaultdict
from subprocess import Popen


class ResultData(object):
    def __init__(self):
        super().__init__()
        self._compile_results = None
        self._scores = defaultdict(dict)
        self._outputs = {}

    def update_compile_result(self, results):
        self._compile_results = results

    def get_compile_results(self):
        return (self._compile_results == b''), self._compile_results

    def add(self, test_id, score):
        self._scores[test_id] = score

    def add_output(self, test_id, output):
        if isinstance(output, bytes):
            output = output.decode('utf-8')
        self._outputs[test_id] = output

    def total_score(self):
        return sum(self._scores.values())

    def summary(self):
        result_statistics = {
            'total_score': self.total_score(),
            'num_test_cases': self._count_num_tests(),
            'compile_result': self._compile_results,
            'tests': self._scores,
            'outputs': self._outputs
        }
        return result_statistics

    def _count_num_tests(self):
        return len(self._scores)

    def __repr__(self):
        summary = self.summary()
        return f"summary: {summary['total_score']} ({summary['compile_result']})"


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
    def run(self, inputs, *args, **kwargs) -> Popen:
        raise NotImplementedError

    def update_compile_results(self, results):
        self._test_results.update_compile_result(results)

    def update_score(self, test_case_id, score):
        self._test_results.add(test_case_id, score)

    def update_output(self, test_case_id, output):
        self._test_results.add_output(test_case_id, output)

    def get_results(self):
        return self._test_results
