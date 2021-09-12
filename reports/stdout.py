def print_to_stdout(test_results):
    for student_id, test_result in test_results.items():
        print(f"student id: {student_id}, {repr(test_result)}")
