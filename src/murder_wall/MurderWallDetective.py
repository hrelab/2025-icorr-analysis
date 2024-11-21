from murder_wall.MurderWallAsset import MurderWallAsset
from typing import List


class MurderWallDetective:
    def __init__(self, murder_wall: List[List[MurderWallAsset]]):
        self.murder_wall: List[List[MurderWallAsset]] = murder_wall
        self.rows: int = len(murder_wall)
        self.columns: int = len(murder_wall[0])

    def get_activity(self, index: int) -> List[MurderWallAsset]:
        assert (self.columns > index)
        return [row[index] for row in self.murder_wall]

    def get_subject(self, index) -> List[MurderWallAsset]:
        assert (self.rows > index)
        return self.murder_wall[index]

    def get_columns(self) -> List[str]:
        return [column for column in self.murder_wall[0][0].get_emg_frame().columns]
