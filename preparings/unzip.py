import os
from zipfile import ZipFile, is_zipfile


def unzip(zip_file_path, extracted_file_path=None):
    extracted_file_path = extracted_file_path if extracted_file_path else zip_file_path.rstrip('.zip')
    with ZipFile(zip_file_path) as zip_file:
        zip_file.extractall(extracted_file_path)
    return extracted_file_path


def unzip_all(extracted_file_path):
    all_files = [os.path.join(extracted_file_path, file_path) for file_path in os.listdir(extracted_file_path)]
    student_submission_zips = [file_path for file_path in all_files if is_zipfile(file_path)]
    extracted_file_paths = []
    for submission_zip in student_submission_zips:
        submission_zip = os.path.join(extracted_file_path, submission_zip)
        extracted_file_paths.append(unzip(submission_zip))
    return extracted_file_paths
