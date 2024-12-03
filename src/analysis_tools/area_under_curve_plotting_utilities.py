import pandas as pd
import matplotlib.pyplot as plt
from murder_wall.murderwall_asset import MurderWallAsset
from typing import List, Callable
from itertools import chain, cycle
import numpy as np
import seaborn as sns
from dataclasses import dataclass
from gstd.working_data import WorkingData


@dataclass
class ActivityUnderConditions:
    right_handed: List[MurderWallAsset]
    left_handed: List[MurderWallAsset]
    impaired_left_handed: List[MurderWallAsset]
    impaired_right_handed: List[MurderWallAsset]


def plot_no_save(area_under_curve_data: pd.DataFrame, plot_title: str, store_at: str, x_label: str, colors: List[str], labels: List[str], labels_per_column: int = 1, clip: int = -1):
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

    x_positions = {category: pos for pos, category in enumerate(area_under_curve_data.columns)}

    for col in area_under_curve_data.columns:
        values = area_under_curve_data[col].dropna()
        if len(values) == 1:  # Check for single data points
            ax.scatter(
                x=[x_positions[col]],  # Correct x-position
                y=values.values,      # Single data point value
                color=palette[col],   # Match the palette color
                s=300,                # Adjust the size of the point
                edgecolor='black',    # Add a border for visibility
                linewidth=2,
                zorder=10,            # Place above other elements
            )

    # we should rename clip here, it makes sense but has already been assigned to shortening the length of a frame relative to another frame.
    if labels_per_column > 1:
        tick_positions = np.arange(0.5, len(area_under_curve_data.columns), labels_per_column)
        if clip > 0:
            tick_labels = [area_under_curve_data.columns[i][:clip] for i in range(1, len(area_under_curve_data.columns), labels_per_column)]
        else:
            tick_labels = [area_under_curve_data.columns[i] for i in range(1, len(area_under_curve_data.columns), labels_per_column)]
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
