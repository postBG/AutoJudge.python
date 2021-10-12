import hydra
from omegaconf import OmegaConf

from preparings.unzip import unzip_all
from preparings.utils import to_project_roots
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
    project_roots = to_project_roots(student_submission_roots)
    submissions = [JavaSubmission(project_root) for project_root in project_roots]
    submission_manager = SubmissionManager(submissions)

    test_cases = test_cases_factory(configs)
    print(f"{len(test_cases)} Test Cases Detected.")

    print(f"Compile Started!")
    submission_manager.compile_all()
    print(f"Compile Ended!")

    print(f"Test Started!")
    submission_manager.run_all(test_cases)
    print(f"Test Ended!")

    test_results = {submission.student_id: submission.get_results() for submission in submissions}
    export_as_csv(test_results, len(test_cases), configs.result_path)
    print_to_stdout(test_results)


if __name__ == '__main__':
    main()
