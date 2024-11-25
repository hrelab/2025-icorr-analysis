from dataclasses import dataclass


@dataclass
class Subject:
    id: str
    age: int
    handedness: str
    impaired: bool
    gender: str
