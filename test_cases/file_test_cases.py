import os
from collections import OrderedDict

from test_cases.abc import AbstractBaseTestCases, TestCase

_BAD_FILES = ['.DS_Store']


def read_file(inputs_path):
    input_example_files = [f for f in os.listdir(inputs_path) if f not in _BAD_FILES]
    inputs = OrderedDict()
    for input_example_file in input_example_files:
        with open(os.path.join(inputs_path, input_example_file), 'rb') as f:
            args = f.read().replace(b'\r', b'').lstrip(b'\n')
            inputs[input_example_file] = args
    return inputs


class SimpleFileTestCases(AbstractBaseTestCases):
    def __init__(self, test_cases_root):
        super().__init__()
        self._test_cases_root = test_cases_root
        self._answers_root = os.path.join(test_cases_root, 'answers')
        self._inputs_root = os.path.join(test_cases_root, 'inputs')
        self._examples = self._construct_test_cases(self._inputs_root, self._answers_root)

    def _construct_test_cases(self, inputs_path, answers_path):
        inputs = read_file(inputs_path)
        outputs = read_file(answers_path)
        self._validate_files(inputs, outputs)

        examples = []
        for file_name, input in inputs.items():
            examples.append(TestCase(input, outputs[file_name], test_id=file_name))
        return examples

    def __getitem__(self, test_case_idx) -> TestCase:
        return self._examples[test_case_idx]

    def __len__(self):
        return len(self._examples)

    def _validate_files(self, inputs, answers):
        assert len(inputs) == len(answers), "The number of the inputs and answers are not matched."
        for k in inputs.keys():
            try:
                answers[k]
            except KeyError as e:
                raise FileNotFoundError(f"The answer of {k} is missing.") from e
