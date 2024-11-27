from src.murder_wall.murderwall import MurderWall
from src.murder_wall.murderwall_detective import MurderWallDetective
from src.analysis_tools.patient_data_extractor import get_subjects
from src.analysis_tools.area_under_curve_plotting_utilities import (
    compute_area_under_curve_plot_for_activity,
    merge_area_under_curve_plots,
    plot_no_save,
    break_into_seperate_conditions,
    merge_condition_plots,
    compute_area_under_curve_plot_for_attribute,
    ActivityUnderConditions,
    LabelsPerColumn
)
from src.murder_wall.experiment_parameters import ExperimentParameters
from src.gstd.WorkingData import WorkingData
import pandas as pd


def make_emg_area_under_curve_on_different_attributes_plots(subject_data: MurderWallDetective):
    def handle_atrributes_under_condition(attributes_under_condition: ActivityUnderConditions, subject_data: MurderWallDetective, activity_index: int, condition: str):
        right_handed_auc = compute_area_under_curve_plot_for_attribute(attributes_under_condition.right_handed)
        left_handed_auc = compute_area_under_curve_plot_for_attribute(attributes_under_condition.left_handed)
        impaired_auc = compute_area_under_curve_plot_for_attribute(attributes_under_condition.impaired)
        merged_data = merge_condition_plots(right_handed_auc, left_handed_auc, impaired_auc)
        plot_no_save(
            merged_data,
            f"Activity {subject_data.get_activity_id(2 * activity_index)} | Condition  {condition}",
            f"../test_data/plot_3/activity_{subject_data.get_activity_id(2 * activity_index)}_condition_{condition}",
            "Muscle",
            ["#984ea3", "#ff7f00", "#ff7ea3"],
            ["Right Handed", "Left Handed", "Impaired"],
            LabelsPerColumn.TRIPLEUP,
            2
        )
    for i, conditions in enumerate(subject_data.get_clipped_activity_pairs()):
        condition_1, condition_2 = conditions
        attributes_condition_1 = break_into_seperate_conditions(condition_1)
        attributes_condition_2 = break_into_seperate_conditions(condition_2)
        handle_atrributes_under_condition(attributes_condition_1, subject_data, i, "01")
        handle_atrributes_under_condition(attributes_condition_2, subject_data, i, "02")


def make_emg_area_under_curve_on_different_activities_plots(subject_data: MurderWallDetective):
    def make_plot_for_certain_muscle(subject_data: MurderWallDetective, condition_data: pd.DataFrame, condition_id: str):
        for muscle in [f"{column}_C{condition_id}" for column in subject_data.get_columns()[3:]]:
            merged_data = pd.DataFrame({f"Activity {subject_data.get_activity_id(2 * i)}": frame[muscle] for i, frame in enumerate(condition_data)})
            plot_no_save(merged_data, f"Muscle {muscle[:-4]} | Condition {condition_id}", f"../test_data/plot_2/{muscle}", "Activity", ["#984ea3"], [])
    condition_1_values, condition_2_values = (
        WorkingData([activity for activity in subject_data.get_clipped_activity_pairs()])
        .map(lambda conditions: (compute_area_under_curve_plot_for_activity(conditions[0]), compute_area_under_curve_plot_for_activity(conditions[1])))
        .unzip()
    )
    make_plot_for_certain_muscle(subject_data, condition_1_values.to_list(), "01")
    make_plot_for_certain_muscle(subject_data, condition_2_values.to_list(), "02")


def make_emg_area_under_curve_on_different_conditions_plots(subject_data: MurderWallDetective):
    for i, conditions in enumerate(subject_data.get_clipped_activity_pairs()):
        condition_1, condition_2 = conditions
        area_under_curve_condition_1 = compute_area_under_curve_plot_for_activity(condition_1)
        area_under_curve_condition_2 = compute_area_under_curve_plot_for_activity(condition_2)
        merged_data = merge_area_under_curve_plots(area_under_curve_condition_1, area_under_curve_condition_2)
        plot_no_save(
            merged_data,
            f"Activity {subject_data.get_activity_id(2 * i)}",
            f"../test_data/plot_1/activity_{subject_data.get_activity_id(2 * i)}",
            "Muscle (Condition 1, Condition 2)",
            ["#984ea3", "#ff7f00"],
            ["Condition 1", "Condition 2"],
            LabelsPerColumn.DOUBLEUP,
            2
        )


def main():
    experiment_parameters: ExperimentParameters = ExperimentParameters(
        activities=[f"0{n}" for n in range(1, 9)],
        conditions=["01", "02"],
        subjects=get_subjects("../proc_data"),
        data_types=["emg", "force"]
    )
    murder_wall: MurderWall = MurderWall(experiment_parameters)
    subject_data: MurderWallDetective = murder_wall.create_layout()
    make_emg_area_under_curve_on_different_conditions_plots(subject_data)
    make_emg_area_under_curve_on_different_activities_plots(subject_data)
    make_emg_area_under_curve_on_different_attributes_plots(subject_data)


if __name__ == "__main__":
    main()
