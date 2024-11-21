from murder_wall.MurderWallAsset import MurderWallAsset
from murder_wall.MurderWallDetective import MurderWallDetective
from murder_wall.TrialDataPath import TrialDataPath
from murder_wall.TrialData import TrialData
from itertools import chain
from typing import List


class MurderWall:
    def __init__(self, subject_ids: List[str]):
        self.subjects = subject_ids
        self.activities = [f"0{n}" for n in range(1, 9)]
        self.conditions = ["01", "02"]
        self.data_types = ["emg", "force"]

    def _create_condition_column(self, activity_data: TrialData) -> MurderWallAsset:
        data_path = TrialDataPath("../proc_data", self.data_types, activity_data)
        return MurderWallAsset(data_path.get_data_frame(), data_path.get_path(), activity_data)

    def _create_activity_column(self, subject_id: str, activity_id: str) -> List[MurderWallAsset]:
        activity_data = [TrialData(subject_id, condition_id, activity_id) for condition_id in self.conditions]
        return [self._create_condition_column(data) for data in activity_data]

    def _create_subject_row(self, subject_id: str) -> List[MurderWallAsset]:
        return list(chain.from_iterable([self._create_activity_column(subject_id, activity_id) for activity_id in self.activities]))

    def create_layout(self) -> MurderWallDetective:
        return MurderWallDetective([self._create_subject_row(subject_id) for subject_id in self.subjects])
