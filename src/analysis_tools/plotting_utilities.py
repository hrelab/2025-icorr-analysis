import seaborn as sns
from typing import List, Dict, Callable, Tuple
from pandas import DataFrame
import matplotlib.pyplot as plt
from itertools import cycle
from statannotations.Annotator import Annotator
import matplotlib.patches as mpatches


def vector_with_no_duplicates(vector: List):
    v = []
    for item in vector:
        if item not in v:
            v.append(item)
    return v


def partition_interval(start: int, stop: int, partition_segment_length: int) -> List[List[int]]:
    return [list(range(i, i + partition_segment_length)) for i in range(start, stop, partition_segment_length)]


def calculate_midpoint_for_partioned_interval(partitioned_interval: List[List[int]]) -> List[int]:
    def midpoint(p_0, p_n):
        return (p_0 + p_n) / 2
    interval = [midpoint(interval[0], interval[-1]) for interval in partitioned_interval]
    return interval


def make_boxplot(x: str, y: str, ax, data: DataFrame, palette: Dict[str, str]):
    sns.boxplot(
        x=x,
        y=y,
        data=data,
        width=0.6,
        showfliers=False,
        linewidth=5,
        hue=x,
        palette=palette,
        ax=ax
    )


def make_scatter(x: str, y: str, ax, data: DataFrame, palette: Dict[str, str]):
    sns.scatterplot(
        x=x,
        y=y,
        hue=x,
        palette=palette,
        data=data,
        s=300,
        ax=ax,
        legend=False
    )


def handle_x_axis(sub_group_length: int, data_frame: DataFrame, ax, label_maker: Callable[[str], str]):
    tick_positions = ax.get_xticks()
    ax.set_xticks(calculate_midpoint_for_partioned_interval(partition_interval(tick_positions[0], tick_positions[-1] + 1, sub_group_length)))
    ax.set_xticklabels(vector_with_no_duplicates(map(label_maker, data_frame.columns)))


def x_axis_no_duplicates(sub_group_length: int, data_frame: DataFrame, ax, label_maker: Callable[[str], str]):
    tick_positions = ax.get_xticks()
    ax.set_xticks(calculate_midpoint_for_partioned_interval(partition_interval(tick_positions[0], tick_positions[-1] + 1, sub_group_length)))
    ax.set_xticklabels(list(map(label_maker, data_frame.columns)))


def handle_legend(labels: List[str], colors: List[str], title: str, ax):
    patches = [mpatches.Patch(color=c, label=l) for c, l in zip(colors, labels)]
    ax.legend(
        handles=patches,
        title=title,
        loc="upper right",
        ncol=1,
        title_fontsize=30,
        fontsize=30,
        facecolor='white',
    )


def custum_legend(legend_values: Dict[str, str], title: str, ax):
    patches = [mpatches.Patch(color=color, label=label) for label, color in legend_values.items()]
    ax.legend(
        handles=patches,
        title=title,
        loc="upper right",
        ncol=1,
        title_fontsize=30,
        fontsize=30,
        facecolor='white',
    )


def setup_plot(x_label: str, title: str):
    plt.figure(figsize=(40, 15))
    plt.ylabel("sEMG AUC", labelpad=30)
    plt.xlabel(x_label, labelpad=30)
    plt.title(title)
    plt.tight_layout()


def plot_group(i: int, data_frame: DataFrame, palette, ax, plotters: List[Callable]):
    box_columns = data_frame.columns[i - 2:i]
    scatter_columns = data_frame.columns[i:i + 2]
    box_data = data_frame[box_columns].melt(var_name='Variable', value_name='Value')
    scatter_data = data_frame[scatter_columns].melt(var_name="Variable", value_name="Value")
    plotters[0]("Variable", "Value", ax, box_data, palette)
    plotters[1]("Variable", "Value", ax, scatter_data, palette)


def annotate_plot(
        data_frame: DataFrame,
        ax,
        pairs: List[tuple],
        test: str
):
    data_melted = data_frame.melt(var_name="Variable", value_name="Value")
    annotator = Annotator(ax, pairs, data=data_melted, x="Variable", y="Value")
    annotator.configure(test=test, text_format="star", loc="inside", verbose=2, hide_non_significant=True)
    annotator.apply_and_annotate()


def plot_chunk(
        data_frame: DataFrame,
        colors: List[str],
        labels: List[str],
        plotters: List[Callable],
        title: str,
        x_label: str,
        save_as: str,
        save_in_formats: List[str],
        sub_group_length: int = 1,
        show_legend: bool = False,
        label_maker: Callable[[str], str] = lambda x: x,
        pairs: List[Tuple] = [],
        test: str = None,
        handle_axis: Callable = handle_x_axis,
        custom_legend: Dict = None
):
    palette = dict(zip(data_frame.columns, cycle(colors)))
    sns.set(style='darkgrid', rc={
        'axes.facecolor': '#F0F0F0',
        'font.size': 50,  # General font size
        'axes.titlesize': 50,  # Title font size
        'axes.labelsize': 40,  # Label font size
        'xtick.labelsize': 30,  # X-axis tick label font size
        'ytick.labelsize': 30,  # Y-axis tick label font size
    })
    data_frame.to_csv(f"{save_as}.csv")
    setup_plot(x_label, title)
    ax = plt.gca()
    for i in [i for i in range(2, len(data_frame.columns), 4)]:
        plot_group(i, data_frame, palette, ax, plotters)
    handle_axis(sub_group_length, data_frame, ax, label_maker)
    if len(pairs) != 0 and test is not None:
        annotate_plot(data_frame, ax, pairs, test)
    if show_legend and custom_legend is None:
        handle_legend(labels, colors, "", ax)
    if show_legend and custom_legend is not None:
        custum_legend(custom_legend, "", ax)
    for file_format in save_in_formats:
        plt.savefig(f"{save_as}.{file_format}")
    plt.close()
