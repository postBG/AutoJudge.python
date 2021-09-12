import csv


def export_as_csv(test_results, num_problems, result_path):
    csv_path = f'{result_path}.csv'
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        wr = csv.writer(f)
        header = ["student id"] + [f'problem{i}' for i in range(num_problems)] + ["score"]
        wr.writerow(header)
        for student_id, test_result in test_results.items():
            content = [student_id]
            content += [test_result.total_score(i) for i in range(num_problems)]
            content.append(test_result.total_score())
            wr.writerow(content)