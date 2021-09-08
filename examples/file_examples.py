import os
from collections import OrderedDict

from examples.abc import AbstractBaseExamples, Example


def read_file(inputs_path):
    input_example_files = os.listdir(inputs_path)
    inputs = OrderedDict()
    for input_example_file in input_example_files:
        with open(os.path.join(inputs_path, input_example_file), 'rb') as f:
            args = f.read().replace(b'\r', b'').lstrip(b'\n')
            inputs[input_example_file] = args
    return inputs


class SimpleFileExamples(AbstractBaseExamples):
    def __init__(self, examples_root):
        super().__init__()
        self._examples_root = examples_root
        self._answers_root = os.path.join(examples_root, 'answers')
        self._inputs_root = os.path.join(examples_root, 'inputs')
        self._examples = self._construct_examples(self._inputs_root, self._answers_root)

    def _construct_examples(self, inputs_path, answers_path):
        inputs = read_file(inputs_path)
        outputs = read_file(answers_path)
        self._validate_files(inputs, outputs)

        examples = []
        for k, input in inputs.items():
            examples.append(Example(input, outputs[k]))
        return examples

    def __getitem__(self, example_idx) -> Example:
        return self._examples[example_idx]

    def __len__(self):
        return len(self._examples)

    def _validate_files(self, inputs, answers):
        assert len(inputs) == len(answers), "The number of the inputs and answers are not matched."
        for k in inputs.keys():
            try:
                answers[k]
            except KeyError as e:
                raise FileNotFoundError(f"The answer of {k} is missing.") from e
