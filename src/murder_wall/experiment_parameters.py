from dataclasses import dataclass
from typing import List


@dataclass
class ExperimentParameters:
    activities: List[str]
    conditions: List[str]
    subjects: List[str]
    data_types: List[str]
