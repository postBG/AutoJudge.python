from test_cases.abc import AbstractBaseTestCases, TestCase


class SimpleManualTestCases(AbstractBaseTestCases):
    def __init__(self, answer_func, inputs):
        super().__init__()
        self.answer_func = answer_func
        self._test_cases = [TestCase(input, self.answer_func(input)) for input in inputs]

    def __getitem__(self, test_case_idx) -> TestCase:
        return self._test_cases[test_case_idx]

    def __len__(self):
        return len(self._test_cases)


class Assignment0ManualTestCases(AbstractBaseTestCases):
    def __init__(self):
        super().__init__()
        inputs = [0.0, 1.0, -2.0, -32.0, 36.5, 72.9, 100, -100, -73]
        bytes_inputs = [bytes(str(i), "utf-8") for i in inputs]
        self._simple_test_cases = SimpleManualTestCases(Assignment0ManualTestCases.assignment0_answer_function,
                                                        bytes_inputs)

    def __getitem__(self, test_case_idx) -> TestCase:
        return self._simple_test_cases[test_case_idx]

    def __len__(self):
        return len(self._simple_test_cases)

    @staticmethod
    def assignment0_answer_function(cel_temp: bytes):
        cel_temp = float(cel_temp)
        return bytes("{:.2f}\n".format(cel_temp * 1.8 + 32), "utf-8")
