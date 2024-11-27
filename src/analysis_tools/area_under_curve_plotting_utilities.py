import pandas as pd
import matplotlib.pyplot as plt
from murder_wall.murderwall_asset import MurderWallAsset
from typing import List
from itertools import chain, cycle
import numpy as np
import seaborn as sns
from dataclasses import dataclass
from gstd.WorkingData import WorkingData
from enum import Enum


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
    area_under_curve_data.to_csv(f"{store_at}.csv")
    plt.close()


class LabelsPerColumn(Enum):
    SINGLEUP = 0
    DOUBLEUP = 1
    TRIPLEUP = 2


def plot_no_save(area_under_curve_data: pd.DataFrame, plot_title: str, store_at: str, x_label: str, colors: List[str], labels: List[str], labels_per_column: LabelsPerColumn = LabelsPerColumn.SINGLEUP, clip: int = -1):
    area_under_curve_data.to_csv(f"{store_at}.csv")
    test_df = area_under_curve_data.melt(var_name='type', value_name='value')
    palette = dict(zip(area_under_curve_data.columns, cycle(colors)))

    plt.figure(figsize=(40, 15))

    sns.set(style='darkgrid', rc={
        'axes.facecolor': '#F0F0F0',
        'font.size': 50,  # General font size
        'axes.titlesize': 50,  # Title font size
        'axes.labelsize': 40,  # Label font size
        'xtick.labelsize': 30,  # X-axis tick label font size
        'ytick.labelsize': 30,  # Y-axis tick label font size
    })

    ax = sns.boxplot(
        data=test_df,
        x='type',
        y='value',
        hue='type',
        palette=palette,
        width=0.6,
        showfliers=False,
        linewidth=5,
    )

    jump_rate = 1
    match labels_per_column:
        case LabelsPerColumn.DOUBLEUP:
            jump_rate = 2
        case LabelsPerColumn.TRIPLEUP:
            jump_rate = 3

    # we should rename clip here, it makes sense but has already been assigned to shortening the length of a frame relative to another frame.
    if labels_per_column != LabelsPerColumn.SINGLEUP:
        tick_positions = np.arange(0.5, len(area_under_curve_data.columns), jump_rate)
        if clip > 0:
            tick_labels = [area_under_curve_data.columns[i][:clip] for i in range(1, len(area_under_curve_data.columns), jump_rate)]
        else:
            tick_labels = [area_under_curve_data.columns[i] for i in range(1, len(area_under_curve_data.columns), jump_rate)]
        ax.set_xticks(tick_positions)
        ax.set_xticklabels(tick_labels, ha='center')

    handles = [plt.Line2D([0], [0], color=colors[i], lw=4, label=labels[i]) for i in range(len(labels))]

    L = ax.legend(
        handles=handles,
        loc='best',
        ncol=1,
        title_fontsize=30,
        fontsize=30,
        facecolor='white',
    )

    plt.setp(L.texts, fontsize=30)
    plt.title(plot_title)
    plt.ylabel("sEMG AUC", labelpad=30)
    plt.xlabel(x_label, labelpad=30)
    plt.tight_layout()
    plt.savefig(f"{store_at}.png")
    plt.close()


def compute_area_under_curve_plot_for_activity(activity: List[MurderWallAsset]) -> pd.DataFrame:
    condition_id = activity[0].metadata.condition
    columns = activity[0].get_emg_frame().columns.tolist()[3:]
    area_under_curve_data_frame = pd.DataFrame(columns=columns)
    for subject_doing_activity in activity:
        subject_emg_activity = subject_doing_activity.get_emg_frame().iloc[:, 3:]
        area_under_curve = subject_emg_activity.cumsum()
        assert len(area_under_curve) >= 1, "sEMG curve cannot have zero area accumulation"
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


@dataclass
class ActivityUnderConditions:
    right_handed: List[MurderWallAsset]
    left_handed: List[MurderWallAsset]
    impaired: List[MurderWallAsset]


def break_into_seperate_conditions(activity: List[MurderWallAsset]) -> ActivityUnderConditions:
    activity = WorkingData(activity)
    left_handed = (
        activity
        .filter(lambda asset: asset.metadata.subject.handedness == "Left" and not asset.metadata.subject.impaired)
        .to_list()
    )
    right_handed = (
        activity
        .filter(lambda asset: asset.metadata.subject.handedness == "Right" and not asset.metadata.subject.impaired)
        .to_list()
    )
    impaired = (
        activity
        .filter(lambda asset: asset.metadata.subject.impaired)
        .to_list()
    )
    return ActivityUnderConditions(right_handed, left_handed, impaired)


def compute_area_under_curve_plot_for_attribute(activity: List[MurderWallAsset]) -> pd.DataFrame:
    attribute = "I" if activity[0].metadata.subject.impaired else activity[0].metadata.subject.handedness[0]
    columns = activity[0].get_emg_frame().columns.tolist()[3:]
    area_under_curve_data_frame = pd.DataFrame(columns=columns)
    for subject_doing_activity in activity:
        subject_emg_activity = subject_doing_activity.get_emg_frame().iloc[:, 3:]
        area_under_curve = subject_emg_activity.cumsum()
        assert len(area_under_curve) >= 1, "sEMG curve cannot have zero area accumulation"
        area_under_curve_data_frame.loc[len(area_under_curve_data_frame)] = area_under_curve.iloc[-1] / len(subject_emg_activity)
    columns_with_condition = [f"{column}_A{attribute}" for column in columns]
    rename_map = dict(zip(columns, columns_with_condition))
    area_under_curve_data_frame = area_under_curve_data_frame.rename(columns=rename_map)
    return area_under_curve_data_frame


def merge_condition_plots(right_handed: pd.DataFrame, left_handed: pd.DataFrame, impaired: pd.DataFrame) -> pd.DataFrame:  # auc = area under curve
    columns_right_handed = right_handed.columns.tolist()
    columns_left_handed = left_handed.columns.tolist()
    columns_impaired = impaired.columns.tolist()
    merged_columns = list(chain.from_iterable(zip(columns_right_handed, columns_left_handed, columns_impaired)))
    merged_tables = pd.concat([right_handed, left_handed, impaired], axis=1)
    merged_tables = merged_tables[merged_columns]
    return merged_tables
