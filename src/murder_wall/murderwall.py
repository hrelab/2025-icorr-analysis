from .murderwall_asset import MurderWallAsset
from .murderwall_detective import MurderWallDetective
from .trial_data_path import TrialDataPath
from .trial_data import TrialData
from .experiment_parameters import ExperimentParameters
from .subject import Subject
from itertools import chain
from typing import List


class MurderWall:
    """
        Orders data in the same fashion as our murder wall. Makes things a little easier to think about (sometimes).
    """

    def __init__(self, experiment_parameters: ExperimentParameters):
        self.experiment_parameters: ExperimentParameters = experiment_parameters

    def _create_condition_column(self, activity_data: TrialData) -> MurderWallAsset:
        data_path = TrialDataPath("./processed_data", self.experiment_parameters.data_types, activity_data)
        return MurderWallAsset(data_path.get_data_frame(), data_path.get_path(), activity_data)

    def _create_activity_column(self, subject_id: str, activity_id: str) -> List[MurderWallAsset]:
        activity_data = [TrialData(Subject.from_id(subject_id), condition_id, activity_id) for condition_id in self.experiment_parameters.conditions]
        return [self._create_condition_column(data) for data in activity_data]

    def _create_subject_row(self, subject_id: str) -> List[MurderWallAsset]:
        return list(chain.from_iterable([self._create_activity_column(subject_id, activity_id) for activity_id in self.experiment_parameters.activities]))

    def create_layout(self) -> MurderWallDetective:
        """
            Creates a MurderWallDetective that has access to the ordered data. The murderwall detective can act on this data.
        """
        return MurderWallDetective([self._create_subject_row(subject_id) for subject_id in self.experiment_parameters.subjects])
