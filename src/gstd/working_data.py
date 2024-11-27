from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, Callable, TypeVar, Tuple, List, Iterable
from functools import reduce
from itertools import islice


T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")


@dataclass
class WorkingData(Generic[T]):
    """
        This should be how python implements the List structure.
        Just like every other good language...
        More features will be added when I need them.
        - Gabe :)
    """
    data: Iterable[T]

    def __iter__(self):
        return self.data

    def map(self, f: Callable[[T], U]) -> WorkingData[U]:
        return WorkingData(map(f, self.data))

    def filter(self, f: Callable[[T], bool]) -> WorkingData[T]:
        return WorkingData(filter(f, self.data))

    def fold(self, f: Callable[[U, T], U], initial: U) -> U:
        return reduce(f, self.data, initial)

    def take(self, n: int) -> WorkingData[T]:
        return WorkingData(islice(self.data, n))

    def slice(self, start: int, stop: int) -> WorkingData[T]:
        return WorkingData(islice(self.data, start, stop))

    def unzip(self) -> Tuple[WorkingData[U], WorkingData[V]]:
        data_1, data_2 = zip(*self.data)
        return (WorkingData(data_1), WorkingData(data_2))

    def to_list(self) -> List[T]:
        return list(self.data)
