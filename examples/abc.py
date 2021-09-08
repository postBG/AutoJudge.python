import abc
from typing import Tuple


class Example(object):
    def __init__(self, input: bytes, answer: bytes, score: float = 1):
        super().__init__()
        self._input = input
        self._answer = answer
        self._score = score

    @property
    def input(self):
        return self._input

    @property
    def answer(self):
        return self._answer

    @property
    def score(self):
        return self._score

    def get_score(self, value):
        return self._score if value == self._answer else 0


class AbstractBaseExamples(abc.ABC):
    @abc.abstractmethod
    def __getitem__(self, example_idx) -> Example:
        raise NotImplementedError

    @abc.abstractmethod
    def __len__(self):
        raise NotImplementedError
