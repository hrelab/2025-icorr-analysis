from murder_wall.murderwall_detective import MurderWallDetective
from murder_wall.murderwall_asset import MurderWallAsset
from analysis_tools.area_under_curve_plotting_utilities import (
    break_into_seperate_conditions,
    merge_data_frames,
    ActivityUnderConditions,
    compute_area_under_curve
)
from gstd.working_data import WorkingData
from analysis_tools.plotting_utilities import plot_chunk, make_boxplot, make_scatter
from os.path import join


def create_label(trial: MurderWallAsset) -> str:
    if trial.metadata.subject.impaired:
        return "ARI" if trial.metadata.subject.handedness == "Right" else "ALI"
    else:
        return f"A{trial.metadata.subject.handedness[0]}"


def create_title(activity_id: str, condition_id: str) -> str:
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
    condition_id = "A" if condition_id == "01" else "B"
    return f"Activity {rename[activity_id]} | Condition  {condition_id}"


def handle_atrributes_under_condition(attributes_under_condition: ActivityUnderConditions, subject_data: MurderWallDetective, activity_index: int, condition: str):
    right_handed_auc = compute_area_under_curve(attributes_under_condition.right_handed, create_label)
    left_handed_auc = compute_area_under_curve(attributes_under_condition.left_handed, create_label)
    impaired_left_handed_auc = compute_area_under_curve(attributes_under_condition.impaired_left_handed, create_label)
    impaired_right_handed_auc = compute_area_under_curve(attributes_under_condition.impaired_right_handed, create_label)
    merged_data = merge_data_frames(WorkingData([right_handed_auc, left_handed_auc, impaired_right_handed_auc, impaired_left_handed_auc]))
    plot_chunk(
        data_frame=merged_data,
        colors=["#293F14", "#729E1A", "#68121B", "#843b3b"],
        labels=["healthy, right handed (RH tested)", "healthy, left handed (RH tested)", "right hand paretic (RH tested)", "left side paretic (LH tested)"],
        plotters=[make_boxplot, make_scatter],
        title=create_title(subject_data.get_activity_id(2 * activity_index), condition),
        x_label="Muscle",
        save_as=join(".", "processed_data_plots", "plot_3", f"activity_{subject_data.get_activity_id(2 * activity_index)}_condition_{condition}"),
        save_in_formats=["png", "pdf"],
        sub_group_length=4,
        show_legend=True,
        label_maker=lambda x: x[:2],
        custom_legend=dict(zip(["healthy, right handed (RH tested)", "healthy, left handed (RH tested)", "right hand paretic (RH tested)", "left side paretic (LH tested)"], ["#293F14", "#729E1A", "#68121B", "#843b3b"]))
    )


def make_plot_3(subject_data: MurderWallDetective):
    for i, conditions in enumerate(subject_data.get_clipped_activity_pairs()):
        condition_1, condition_2 = conditions
        attributes_condition_1 = break_into_seperate_conditions(condition_1)
        attributes_condition_2 = break_into_seperate_conditions(condition_2)
        handle_atrributes_under_condition(attributes_condition_1, subject_data, i, "01")
        handle_atrributes_under_condition(attributes_condition_2, subject_data, i, "02")
