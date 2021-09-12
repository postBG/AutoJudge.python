import abc
from subprocess import Popen


class AbstractBaseSubmission(abc.ABC):
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

    # @abc.abstractmethod
    # def write_compile_results(self, results):
    #     raise NotImplementedError
    #
    # @abc.abstractmethod
    # def get_compile_results(self, results):
    #     raise NotImplementedError
    #
    # @abc.abstractmethod
    # def write_score(self, problem_id, score):
    #     raise NotImplementedError
    #
    # @abc.abstractmethod
    # def get_scores(self):
    #     raise NotImplementedError
