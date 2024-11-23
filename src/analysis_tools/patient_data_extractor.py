from os import listdir
from typing import List


def get_subjects(subject_data_path: str) -> List[str]:
    subjects = listdir(subject_data_path)
    return subjects
