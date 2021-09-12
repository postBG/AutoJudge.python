import os

import hydra
from omegaconf import OmegaConf

from preparings.unzip import unzip_all
from reports.csv import export_as_csv
from reports.stdout import print_to_stdout
from submissions.java_submissions import JavaSubmission
from submissions.submission_manager import SubmissionManager
from test_cases import test_cases_factory


@hydra.main(config_path='configs', config_name='default_setup')
def main(configs):
    OmegaConf.set_struct(configs, False)
    submissions_root = configs.submissions_root
    student_submission_roots = unzip_all(submissions_root)
    student_project_roots = [os.path.join(submission_root, configs.assignment_root_name)
                             for submission_root in student_submission_roots]
    submissions = [JavaSubmission(project_root) for project_root in student_project_roots]
    submission_manager = SubmissionManager(submissions)

    for problem_idx in range(configs.num_problems):
        test_cases = test_cases_factory(configs)

        submission_manager.compile_all(problem_idx)
        submission_manager.run_all(problem_idx, test_cases)

    test_results = {submission.student_id: submission.get_results() for submission in submissions}
    export_as_csv(test_results, configs.num_problems, configs.result_path)
    print_to_stdout(test_results)


if __name__ == '__main__':
    main()
