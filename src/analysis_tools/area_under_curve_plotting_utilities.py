import pandas as pd
from murder_wall.murderwall_asset import MurderWallAsset
from typing import List, Callable
from dataclasses import dataclass
from gstd.working_data import WorkingData
from itertools import chain


@dataclass
class ActivityUnderConditions:
    right_handed: List[MurderWallAsset]
    left_handed: List[MurderWallAsset]
    impaired_left_handed: List[MurderWallAsset]
    impaired_right_handed: List[MurderWallAsset]


def break_into_seperate_conditions(activity: List[MurderWallAsset]) -> ActivityUnderConditions:
    activity_wrapped = WorkingData(activity)
    left_handed = (
        activity_wrapped
        .filter(lambda asset: asset.metadata.subject.handedness == "Left" and not asset.metadata.subject.impaired)
        .to_list()
    )
    right_handed = (
        activity_wrapped
        .filter(lambda asset: asset.metadata.subject.handedness == "Right" and not asset.metadata.subject.impaired)
        .to_list()
    )
    impaired_left_handed = (
        activity_wrapped
        .filter(lambda asset: asset.metadata.subject.impaired and asset.metadata.subject.handedness == "Left")
        .to_list()
    )
    impaired_right_handed = (
        activity_wrapped
        .filter(lambda asset: asset.metadata.subject.impaired and asset.metadata.subject.handedness == "Right")
        .to_list()
    )
    return ActivityUnderConditions(right_handed, left_handed, impaired_left_handed, impaired_right_handed)


def compute_area_under_curve(activity: List[MurderWallAsset], label_format: Callable[[MurderWallAsset], str]) -> pd.DataFrame:
    label = label_format(activity[0])
    columns = activity[0].get_emg_frame().columns.tolist()[3:]
    area_under_curve_data_frame = pd.DataFrame(columns=columns)
    for subject_doing_activity in activity:
        subject_emg_activity = subject_doing_activity.get_emg_frame().iloc[:, 3:]
        area_under_curve = subject_emg_activity.cumsum()
        assert len(area_under_curve) >= 1, "sEMG curve cannot have zero area accumulation"
        area_under_curve_data_frame.loc[len(area_under_curve_data_frame)] = area_under_curve.iloc[-1] / len(subject_emg_activity)
    columns_with_condition = [f"{column}_{label}" for column in columns]
    rename_map = dict(zip(columns, columns_with_condition))
    area_under_curve_data_frame = area_under_curve_data_frame.rename(columns=rename_map)
    return area_under_curve_data_frame


def merge_data_frames(data_frames: WorkingData[pd.DataFrame]) -> pd.DataFrame:  # auc = area under curve
    columns = (
        data_frames
        .map(lambda frame: frame.columns.tolist())
        .to_list()
    )
    merged_columns = list(chain.from_iterable(zip(*columns)))
    merged_tables = pd.concat([frame for frame in data_frames.to_list()], axis=1)
    merged_tables = merged_tables[merged_columns]
    return merged_tables
