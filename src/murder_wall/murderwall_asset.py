from __future__ import annotations
from pandas import DataFrame
from .trial_data import TrialData
from dataclasses import dataclass


@dataclass
class FrameData:
    """
        Holds frame data for a certain trial
    """
    emg_data: DataFrame
    force_data: DataFrame


@dataclass
class PathData:
    """
        Holds path data for a certain trial
    """
    emg_path: str
    force_path: str


@dataclass
class MurderWallAsset:
    """
        Holds frame data, path data, and metadata regarding a certain trial
    """
    frame_data: FrameData
    path_data: PathData
    metadata: TrialData

    def get_emg_frame(self) -> DataFrame:
        return self.frame_data.emg_data

    def get_force_frame(self) -> DataFrame:
        return self.frame_data.force_data

    def get_emg_path(self) -> str:
        return self.path_data.emg_path

    def get_force_path(self) -> str:
        return self.path_data.force_path

    def clip_emg_asset(self, clip_length) -> MurderWallAsset:
        """
            Clips emg data down to the clip length
        """
        assert clip_length > 0
        emg, force = self.get_emg_frame(), self.get_force_frame()
        new_emg = emg.iloc[0:clip_length, :]
        return MurderWallAsset(FrameData(new_emg, force), self.path_data, self.metadata)

    def get_emg_frame_length(self) -> int:
        return len(self.frame_data.emg_data)
