from dataclasses import dataclass
from .subject import Subject


@dataclass
class TrialData:
    subject: Subject
    condition: str
    activity: str
