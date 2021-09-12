import re


def extract_student_id_from(file_name):
    return re.search("\d{4}-\d{5}", file_name).group(0)
