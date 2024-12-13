import os
import pandas as pd
from typing import List
from .trial_data import TrialData
from .murderwall_asset import PathData, FrameData
from os.path import join


class TrialDataPath:
    """
        Creates a path to the pre-proced data being stored for a certain trial.
    """

    def __init__(self, path: str, d_types: List[str], trial_data: TrialData):
        self.path = path
        self.d_types = d_types
        self.trial_data = trial_data

    def _create_path(self, d_type: str) -> str:
        return join(self.path, self.trial_data.subject.id, self.trial_data.condition, f"processed-{d_type}-{self.trial_data.activity}.csv")
        # return f"{self.path}/{self.trial_data.subject.id}/{self.trial_data.condition}/processed-{d_type}-{self.trial_data.activity}.csv"

    def _assert_existence_of_new_data(self, emg: str, force: str):
        assert (os.path.exists(emg))
        assert (os.path.exists(force))

    def _get(self):
        emg, force = self.d_types
        emg_path = self._create_path(emg)
        force_path = self._create_path(force)
        self._assert_existence_of_new_data(emg_path, force_path)
        return (emg_path, force_path)

    def get_path(self) -> PathData:
        """
            Gets the path data for a certain trial
        """
        emg, force = self._get()
        return PathData(emg, force)

    def get_data_frame(self) -> FrameData:
        """
            Loads pandas dataframes for a certain trial
        """
        emg, force = self._get()
        print(f"Converting {emg} to dataframe")
        print(f"Converting {force} to dataframe")
        return FrameData(pd.read_csv(emg, index_col=0), pd.read_csv(force, index_col=0))
