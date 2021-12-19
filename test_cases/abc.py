import abc


class TestCase(object):
    def __init__(self, input: bytes, answer: bytes, score: float = 1, test_id=None):
        super().__init__()
        self._input = input
        self._answer = answer
        self._score = score
        self._test_id = test_id

    @property
    def input(self):
        return self._input

    @property
    def answer(self):
        return self._answer

    @property
    def score(self):
        return self._score

    @property
    def test_id(self):
        return self._test_id

    def get_score(self, value):
        answers_per_lines = self._answer.replace(b'\r', b'').strip(b'\n').decode('utf-8').split('\n')
        values_per_lines = value.replace(b'\r', b'').strip(b'\n').decode('utf-8').split('\n')
        if len(answers_per_lines) != len(values_per_lines):
            return 0

        for l1, l2 in zip(answers_per_lines, values_per_lines):
            if l1.strip() != l2.strip():
                return 0

        return self._score


class AbstractBaseTestCases(abc.ABC):
    @abc.abstractmethod
    def __getitem__(self, test_case_idx) -> TestCase:
        raise NotImplementedError

    @abc.abstractmethod
    def __len__(self):
        raise NotImplementedError
