import os

import hydra
from omegaconf import OmegaConf

from preparings.unzip import unzip_all
from test_cases.file_examples import SimpleFileTestCases
from submissions.java_submissions import compile_code, run_code, JavaSubmission


@hydra.main(config_path='configs', config_name='default_setup')
def main(configs):
    OmegaConf.set_struct(configs, False)
    submissions_root = configs.submissions_root
    student_submission_roots = unzip_all(submissions_root)
    student_project_roots = [os.path.join(submission_root, configs.assignment_root_name)
                             for submission_root in student_submission_roots]
    submissions = [JavaSubmission(project_root) for project_root in student_project_roots]

    for problem_idx in range(configs.num_problems):
        assigment_testcase_root = configs.assigment_testcase_root
        test_cases = SimpleFileTestCases(assigment_testcase_root)

        compile_procs = [submission.compile(problem_idx) for submission in submissions]
        for proc in compile_procs:
            proc.communicate()

        for i, test_case in enumerate(test_cases):
            test_procs = [submission.run(problem_idx, test_case.input) for submission in submissions]
            for proc in test_procs:
                out = proc.communicate()[0]
                print(f'{i}-th score: {test_case.get_score(out)}')


if __name__ == '__main__':
    main()
