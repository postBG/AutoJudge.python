import csv


def export_as_csv(test_results, num_test_cases, result_path):
    csv_path = f'{result_path}.csv'
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        wr = csv.writer(f)
        header = ["student id"] + ["total_num_tests", "total_score"] + [f'test{i}' for i in range(num_test_cases)]
        wr.writerow(header)
        for student_id, test_result in test_results.items():
            summary = test_result.summary()
            test_ids = summary['tests'].keys()
            test_ids.sort()

            content = [student_id, summary['num_test_cases'], summary['total_score']]
            content += [summary['tests'][test_id] for test_id in test_ids]
            wr.writerow(content)
