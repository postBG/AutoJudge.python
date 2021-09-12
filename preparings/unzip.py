import os
import shutil
from zipfile import ZipFile, is_zipfile

BAD_FILENAME = ['__MACOSX', '.DS_Store']


def find_submission_root(extracted_file_path):
    dirs = [dir for dir in os.listdir(extracted_file_path) if dir not in BAD_FILENAME]
    return os.path.join(extracted_file_path, dirs[0])


def remove_bad_files(extracted_file_path):
    for dir in os.listdir(extracted_file_path):
        if dir in BAD_FILENAME:
            target_dir = os.path.join(extracted_file_path, dir)
            shutil.rmtree(target_dir)


def unzip(zip_file_path, extracted_file_path=None):
    extracted_file_path = extracted_file_path if extracted_file_path else zip_file_path.rstrip('.zip')
    with ZipFile(zip_file_path) as zip_file:
        zip_file.extractall(extracted_file_path)
        remove_bad_files(extracted_file_path)
    return extracted_file_path


def unzip_all(extracted_file_path):
    all_files = [os.path.join(extracted_file_path, file_path) for file_path in os.listdir(extracted_file_path)]
    student_submission_zips = [file_path for file_path in all_files if is_zipfile(file_path)]
    extracted_file_paths = []
    for submission_zip in student_submission_zips:
        submission_zip = os.path.join(extracted_file_path, submission_zip)
        extracted_file_paths.append(unzip(submission_zip))
    return extracted_file_paths
