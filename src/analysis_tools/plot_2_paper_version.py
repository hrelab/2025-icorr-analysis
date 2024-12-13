from murder_wall.murderwall_detective import MurderWallDetective
from murder_wall.murderwall_asset import MurderWallAsset
from gstd.working_data import WorkingData
from .area_under_curve_plotting_utilities import compute_area_under_curve, merge_data_frames
from itertools import combinations
from os.path import join
from .plotting_utilities import (
    plot_chunk,
    make_boxplot,
    x_axis_no_duplicates
)


def create_label(trial: MurderWallAsset) -> str:
    return f"{trial.metadata.activity}"


def label_maker(label: str) -> str:
    rename = {
        "01": "x-axis",
        "02": "y-axis",
        "03": "z-axis",
        "04": "torque",
    }
    return rename[label]


def make_plot_2(subject_data: MurderWallDetective):
    clipped_activities = list(map(lambda x: x[0], subject_data.get_clipped_activity_pairs()))
    clipped_activities = clipped_activities[:4]
    area_under_curves = merge_data_frames(
        WorkingData([compute_area_under_curve(activity, create_label) for activity in clipped_activities])
    )
    ad_labels = [f"AD_0{n}" for n in range(1, 5)]
    ex_labels = [f"EX_0{n}" for n in range(1, 5)]
    labels = ad_labels + ex_labels
    area_under_curves = area_under_curves[labels]
    pairs = list(combinations(ad_labels, 2)) + list(combinations(ex_labels, 2))
    color_1 = ["#163E64"]
    color_2 = ["#215F9A"]
    colors = color_1 * 4 + color_2 * 4
    plot_chunk(
        data_frame=area_under_curves,
        colors=colors,
        labels=["AD"] + ["EX"],
        plotters=[make_boxplot, make_boxplot],
        title="Area Under Curve vs Muscle and Activity",
        x_label="Goal Trajectory",
        save_as=join(".", "processed_data_plots", "plot_2_muscle-across-activities", "plot_2_for_paper"),
        save_in_formats=["png", "pdf", "svg"],
        sub_group_length=1,
        show_legend=True,
        label_maker=lambda x: label_maker(x[-2:]),
        pairs=pairs,
        test="Kruskal",
        handle_axis=x_axis_no_duplicates,
        custom_legend=dict([("AD", "#163E64"), ("EX", "#215F9A")])
    )
