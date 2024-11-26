from .murderwall_asset import MurderWallAsset
from typing import List, Tuple


class MurderWallDetective:
    def __init__(self, murder_wall: List[List[MurderWallAsset]]):
        self.murder_wall: List[List[MurderWallAsset]] = murder_wall
        self.rows: int = len(murder_wall)
        self.columns: int = len(murder_wall[0])

    def get_activity(self, index: int) -> List[MurderWallAsset]:
        assert (self.columns > index)
        return [row[index] for row in self.murder_wall]

    def get_subject(self, index: int) -> List[MurderWallAsset]:
        assert (self.rows > index)
        return self.murder_wall[index]

    def get_columns(self) -> List[str]:
        return [column for column in self.murder_wall[0][0].get_emg_frame().columns]

    def get_activity_id(self, index: int) -> str:
        return self.get_activity(index)[0].metadata.activity

    def get_condition_id(self, index: int) -> str:
        return self.get_activity(index)[0].metadata.condition

    def _find_activity_emg_clip_value(self, activity: List[MurderWallAsset]) -> int:
        """
            Find the minimum game across all subjects of a given activity and return the length.
        """
        return min([asset.get_emg_frame_length() for asset in activity])

    def get_clipped_activity_pairs(self) -> Tuple[List[MurderWallAsset], List[MurderWallAsset]]:
        for i in range(0, self.columns, 2):
            activity_condition_1 = self.get_activity(i)
            activity_condition_2 = self.get_activity(i + 1)
            min_value = min(self._find_activity_emg_clip_value(activity_condition_1), self._find_activity_emg_clip_value(activity_condition_2))
            clipped_activity_condition_1 = [asset.clip_emg_asset(min_value) for asset in activity_condition_1]
            clipped_activity_condition_2 = [asset.clip_emg_asset(min_value) for asset in activity_condition_2]
            yield (clipped_activity_condition_1, clipped_activity_condition_2)

    def get_activity_pairs(self):
        for i in range(0, self.columns, 2):
            activity_condition_1 = self.get_activity(i)
            activity_condition_2 = self.get_activity(i + 1)
            yield (activity_condition_1, activity_condition_2)
