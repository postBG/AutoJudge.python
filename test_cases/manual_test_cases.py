import random

from test_cases.abc import AbstractBaseTestCases, TestCase


class SimpleManualTestCases(AbstractBaseTestCases):
    def __init__(self, inputs, answers):
        super().__init__()
        self._test_cases = [TestCase(input, answer) for input, answer in zip(inputs, answers)]

    def __getitem__(self, test_case_idx) -> TestCase:
        return self._test_cases[test_case_idx]

    def __len__(self):
        return len(self._test_cases)


class Assignment0ManualTestCases(AbstractBaseTestCases):
    def __init__(self):
        super().__init__()
        inputs = [0.0, 1.0, -2.0, -32.0, 36.5, 72.9, 100, -100, -73]
        bytes_inputs = [bytes(str(i), "utf-8") for i in inputs]
        answers = [Assignment0ManualTestCases.assignment0_answer_function(input) for input in bytes_inputs]
        self._simple_test_cases = SimpleManualTestCases(bytes_inputs, answers)

    def __getitem__(self, test_case_idx) -> TestCase:
        return self._simple_test_cases[test_case_idx]

    def __len__(self):
        return len(self._simple_test_cases)

    @staticmethod
    def assignment0_answer_function(cel_temp: bytes):
        cel_temp = float(cel_temp)
        return bytes("{:.2f}\n".format(cel_temp * 1.8 + 32), "utf-8")


class Assignment3ManualTestCases(AbstractBaseTestCases):
    def __init__(self):
        super().__init__()
        sortings = ['B', 'I', 'Q', 'T', 'M', 'R']
        sizes = [1, 2, *[random.randint(1, 500) for _ in range(5)]]
        numbers_list = [[random.randint(-100000, 100000) for _ in range(size)] for size in sizes]
        sorted_list = [sorted(numbers) for numbers in numbers_list]

        numbers_list = self.numbers_to_str(numbers_list)
        sorted_numbers_list = self.numbers_to_str(sorted_list)

        inputs = []
        answers = []
        for sorting in sortings:
            for size in sizes:
                for numbers, sorted_numbers in zip(numbers_list, sorted_numbers_list):
                    inputs.append(self.to_str(sorting, size, numbers))
                    answers.append(sorted_numbers)

        bytes_inputs = [bytes(tc, "utf-8") for tc in inputs]
        bytes_answers = [bytes(ans, 'utf-8') for ans in answers]

        self._simple_test_cases = SimpleManualTestCases(bytes_inputs, bytes_answers)

    def to_str(self, sorting, size, numbers):
        return f'{sorting}\n{size}\n{numbers}\n'

    def numbers_to_str(self, numbers_list):
        lst = []
        for numbers in numbers_list:
            numbers = [str(n) for n in numbers]
            lst.append(" ".join(numbers))
        return lst

    def __getitem__(self, test_case_idx) -> TestCase:
        return self._simple_test_cases[test_case_idx]

    def __len__(self):
        return len(self._simple_test_cases)
