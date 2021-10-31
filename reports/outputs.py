import os
from pathlib import Path


def export_outputs(test_results, output_path):
    Path(output_path).mkdir(parents=True, exist_ok=True)

    for student_id, test_result in test_results.items():
        results = test_result.summary()
        student_path = os.path.join(output_path, student_id)
        Path(student_path).mkdir(parents=True, exist_ok=True)
        for test_id, output in results['outputs'].items():
            test_path = os.path.join(student_path, f'{test_id}')
            with open(test_path, 'w') as f:
                f.write(output)
