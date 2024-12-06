from dataclasses import dataclass
from typing import List


@dataclass
class ExperimentParameters:
    """
        Contains important data about the experiement in whole
    """
    activities: List[str]
    conditions: List[str]
    subjects: List[str]
    data_types: List[str]
