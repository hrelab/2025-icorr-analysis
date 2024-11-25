import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from murder_wall.MurderWallAsset import MurderWallAsset
from typing import List
from itertools import chain, cycle


def plot_and_save(area_under_curve_data: pd.DataFrame, plot_title: str, store_at: str, x_label: str, colors : List[str], labels : List[str], position_mult : float, double_up : bool = False, clip : int = -1):
    test_df = area_under_curve_data.melt(var_name='type', value_name='value')
    palette = dict(zip(area_under_curve_data.columns, cycle(colors)))
    # positions = [i*position_mult for i in range(1, len(area_under_curve_data.columns)+1)]

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
        # positions=positions
    )


    if double_up:
        # Calculate positions for labels between every other column
        # tick_positions = positions * 0.5
        tick_positions = np.arange(0.5, len(area_under_curve_data.columns), 2)
        if clip > 0:
            tick_labels = [area_under_curve_data.columns[i][:clip] for i in range(1, len(area_under_curve_data.columns), 2)] # Labels
        else:
            tick_labels = [area_under_curve_data.columns[i] for i in range(1, len(area_under_curve_data.columns), 2)]
        # Set custom x-ticks
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
    plt.savefig(f"{store_at}.pdf")
    plt.close()

def plot_joint_data(impaired_data: pd.DataFrame, unimpaired_data : pd.DataFrame, plot_title: str, store_at: str, x_label: str, colors : List[str], labels : List[str], position_mult : float, double_up : bool = False, clip : int = -1):
    impaired_df = impaired_data.melt(var_name='type', value_name='value')
    unimpaired_df = unimpaired_data.melt(var_name='type', value_name='value')
    palette = dict(zip(impaired_data.columns, cycle(colors)))
    # positions = [i*position_mult for i in range(1, len(area_under_curve_data.columns)+1)]

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
        # positions=positions
    )

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
    plt.savefig(f"{store_at}.pdf")
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
