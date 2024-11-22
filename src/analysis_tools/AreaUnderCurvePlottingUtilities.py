import pandas as pd
import matplotlib.pyplot as plt
from murder_wall.MurderWallAsset import MurderWallAsset
from typing import List
from itertools import chain


def plot_and_save(area_under_curve_data: pd.DataFrame, plot_title: str, store_at: str, x_label: str):
    font = {'size': 20}
    plt.rc('font', **font)
    plt.figure(figsize=(40, 15))
    area_under_curve_data.boxplot(showfliers=False)
    plt.title(plot_title)
    plt.ylabel("Area Under Curve", labelpad=30)
    plt.xlabel(x_label, labelpad=30)
    plt.savefig(f"{store_at}.eps")
    plt.savefig(f"{store_at}.png")
    plt.close()


def compute_area_under_curve_plot_for_activity(activity: List[MurderWallAsset]) -> pd.DataFrame:
    condition_id = activity[0].metadata.condition
    columns = activity[0].get_emg_frame().columns.tolist()[3:]
    area_under_curve_data_frame = pd.DataFrame(columns=columns)
    for subject_doing_activity in activity:
        subject_emg_activity = subject_doing_activity.get_emg_frame().iloc[:, 3:]
        print(f"A: {subject_doing_activity.metadata.activity} | C: {subject_doing_activity.metadata.condition} | S: {subject_doing_activity.metadata.subject} => {len(subject_emg_activity)}")
        area_under_curve = subject_emg_activity.cumsum()
        if len(area_under_curve) < 1:
            continue
        area_under_curve_data_frame.loc[len(area_under_curve_data_frame)] = area_under_curve.iloc[-1] / len(subject_emg_activity)
    columns_with_condition = [f"{column}_C{condition_id}" for column in columns]
    rename_map = dict(zip(columns, columns_with_condition))
    area_under_curve_data_frame = area_under_curve_data_frame.rename(columns=rename_map)
    return area_under_curve_data_frame


def merge_area_under_curve_plots(auc_condition_1: pd.DataFrame, auc_condition_2: pd.DataFrame) -> pd.DataFrame:  # auc = area under curve
    columns_condition_1 = auc_condition_1.columns.tolist()
    columns_condition_2 = auc_condition_2.columns.tolist()
    merged_columns = list(chain.from_iterable(zip(columns_condition_1, columns_condition_2)))
    merged_tables = pd.concat([auc_condition_1, auc_condition_2], axis=1)
    merged_tables = merged_tables[merged_columns]
    return merged_tables
