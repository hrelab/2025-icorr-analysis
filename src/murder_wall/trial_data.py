from dataclasses import dataclass
from .subject import Subject


@dataclass
class TrialData:
    """
        Holds data about a trial.
    """
    subject: Subject
    condition: str
    activity: str
