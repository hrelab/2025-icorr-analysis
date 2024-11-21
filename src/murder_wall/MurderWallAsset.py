from pandas import DataFrame
from typing import Tuple
from murder_wall.TrialData import TrialData


class MurderWallAsset:
    def __init__(self, data_frame: Tuple[DataFrame, DataFrame], file_path: Tuple[str, str], metadata: TrialData):
        self.data_frame = data_frame
        self.file_path = file_path
        self.metadata = metadata

    def __repr__(self):
        return self.metadata.__repr__()

    def get_emg_frame(self) -> DataFrame:
        return self.data_frame[0]

    def get_force_frame(self) -> DataFrame:
        return self.data_frame[1]

    def get_emg_path(self) -> str:
        return self.file_path[0]

    def get_force_path(self) -> str:
        return self.file_path[1]
