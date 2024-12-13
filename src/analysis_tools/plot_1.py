from murder_wall.murderwall_detective import MurderWallDetective
from murder_wall.murderwall_asset import MurderWallAsset
from analysis_tools.area_under_curve_plotting_utilities import (
    merge_data_frames,
    compute_area_under_curve
)
from gstd.working_data import WorkingData
from analysis_tools.plotting_utilities import plot_chunk, make_boxplot
from os.path import join


def create_label(trial: MurderWallAsset) -> str:
    return f"c{trial.metadata.condition}"


def rename_plot_title(activity_id: str) -> str:
    rename = {
        "01": "x-axis",
        "02": "y-axis",
        "03": "z-axis",
        "04": "torque",
        "05": "circle (CW)",
        "06": "circle (CCW)",
        "07": "spline 1",
        "08": "spline 2"
    }
    return f"Activity {rename[activity_id]}"


def make_plot_1(subject_data: MurderWallDetective):
    for i, conditions in enumerate(subject_data.get_clipped_activity_pairs()):
        condition_1, condition_2 = conditions
        area_under_curve_condition_1 = compute_area_under_curve(condition_1, create_label)
        area_under_curve_condition_2 = compute_area_under_curve(condition_2, create_label)
        merged_data = merge_data_frames(WorkingData([area_under_curve_condition_1, area_under_curve_condition_2]))
        columns = list(merged_data.columns)
        pairs = list(zip(columns[::2], columns[1::2]))
        plot_chunk(
            data_frame=merged_data,
            colors=["#984ea3", "#ff7f00"],
            labels=["Condition A", "Condition B"],
            plotters=[make_boxplot, make_boxplot],
            title=rename_plot_title(subject_data.get_activity_id(2 * i)),
            x_label="Muscle",
            save_as=join(".", "processed_data_plots", "plot_1_pose-condition", f"activity_{subject_data.get_activity_id(2 * i)}"),
            save_in_formats=["png", "pdf"],
            sub_group_length=2,
            show_legend=True,
            label_maker=lambda x: x[:2],
            pairs=pairs,
            test="Wilcoxon",
            custom_legend=dict(zip(["Condition A", "Condition B"], ["#984ea3", "#ff7f00"]))
        )
