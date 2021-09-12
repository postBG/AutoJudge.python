import os

import hydra
from omegaconf import OmegaConf

from preparings.unzip import unzip_all
from test_cases.file_examples import SimpleFileTestCases
from java_utils import compile_code, run_code


@hydra.main(config_path='configs', config_name='default_setup')
def main(configs):
    OmegaConf.set_struct(configs, False)
    submissions_root = configs.submissions_root
    student_submission_roots = unzip_all(submissions_root)
    student_project_roots = [os.path.join(submission_root, configs.assignment_root_name)
                             for submission_root in student_submission_roots]
    source_roots = [os.path.join(project_root, configs.source_root) for project_root in student_project_roots]
    production_roots = [os.path.join(project_root, configs.production_root) for project_root in student_project_roots]

    for problem_idx in range(configs.num_problems):
        target_name = configs.target_entry_class
        target_package = f"problem{problem_idx}"
        compile_targets = [os.path.join(source_root, target_package, f"{target_name}.java") for source_root in
                           source_roots]

        assigment_testcase_root = configs.assigment_testcase_root
        test_cases = SimpleFileTestCases(assigment_testcase_root)

        compile_procs = []
        for compile_target, production_root in zip(compile_targets, production_roots):
            proc = compile_code(compile_target, production_root)
            compile_procs.append(proc)

        for proc in compile_procs:
            proc.communicate()

        for i, test_case in enumerate(test_cases):
            test_procs = []
            for student_project_root, production_root in zip(student_project_roots, production_roots):
                proc = run_code(student_project_root, production_root, target_package, target_name, test_case.input)
                test_procs.append(proc)

            for proc in test_procs:
                out = proc.communicate()[0]
                print(f'{i}-th score: {test_case.get_score(out)}')


if __name__ == '__main__':
    main()
