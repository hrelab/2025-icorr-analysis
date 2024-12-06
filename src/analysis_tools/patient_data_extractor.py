from os import listdir
from typing import List


def get_subjects(subject_data_path: str) -> List[str]:
    """
        Easy way to query subjects from the file structure of the pre-proced data.
    """
    subjects = listdir(subject_data_path)
    return subjects
