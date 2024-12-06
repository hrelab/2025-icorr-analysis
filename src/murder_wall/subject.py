from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Subject:
    """
        Holds data about a subject.
    """
    id: str
    gender: str
    age: int
    handedness: str
    impaired: bool

    @staticmethod
    def from_id(id: str) -> Subject:
        """
            Creates a valid subject from an id.

            This should be changed a serialized version from another file.
        """
        match id:
            case "02":
                return Subject("02", "M", 20, "Left", False)
            case "03":
                return Subject("03", "M", 23, "Right", False)
            case "04":
                return Subject("04", "M", 22, "Left", False)
            case "05":
                return Subject("05", "M", 22, "Right", False)
            case "07":
                return Subject("07", "F", 31, "Right", False)
            case "08":
                return Subject("08", "M", 28, "Right", False)
            case "09":
                return Subject("09", "F", 23, "Right", False)
            case "12":
                return Subject("12", "M", 22, "Right", False)
            case "13":
                return Subject("13", "F", 29, "Right", False)
            case "14":
                return Subject("14", "F", 21, "Right", False)
            case "15":
                return Subject("15", "M", 27, "Right", False)
            case "19":
                return Subject("19", "F", 70, "Left", False)
            case "20":
                return Subject("20", "F", 46, "Right", False)
            case "21":
                return Subject("21", "F", 24, "Right", True)
            case "22":
                return Subject("22", "M", 34, "Left", True)
            case _:
                assert False, "Given Subject Does Not Exist"
