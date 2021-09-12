from test_cases.file_test_cases import SimpleFileTestCases
from test_cases.manual_test_cases import Assignment0ManualTestCases


def test_cases_factory(configs):
    code = configs.test_cases_code
    if code == "simple_file":
        return SimpleFileTestCases(configs.assigment_testcase_root)
    elif code == "assignment0_manual":
        return Assignment0ManualTestCases()
    else:
        raise ValueError(f"{code} is not supported.")
