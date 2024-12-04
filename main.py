from src.murder_wall.murderwall import MurderWall
from src.murder_wall.murderwall_detective import MurderWallDetective
from src.murder_wall.murderwall_asset import MurderWallAsset
from src.analysis_tools.patient_data_extractor import get_subjects
from src.analysis_tools.area_under_curve_plotting_utilities import (
    break_into_seperate_conditions,
    merge_data_frames,
    ActivityUnderConditions,
    compute_area_under_curve
)
from src.murder_wall.experiment_parameters import ExperimentParameters
from src.gstd.working_data import WorkingData
from src.analysis_tools.plotting_utilities import plot_chunk, make_boxplot, make_scatter

from src.experimental_setup_plots import (
    dataRelease, expSetupFigures
    )

import pandas as pd


def make_emg_area_under_curve_on_different_attributes_plots(subject_data: MurderWallDetective):
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
            save_as=f"../test_data/plot_3/activity_{subject_data.get_activity_id(2 * activity_index)}_condition_{condition}",
            save_in_formats=["png", "pdf"],
            sub_group_length=4,
            show_legend=True,
            label_maker=lambda x: x[:2]
        )

    for i, conditions in enumerate(subject_data.get_clipped_activity_pairs()):
        condition_1, condition_2 = conditions
        attributes_condition_1 = break_into_seperate_conditions(condition_1)
        attributes_condition_2 = break_into_seperate_conditions(condition_2)
        handle_atrributes_under_condition(attributes_condition_1, subject_data, i, "01")
        handle_atrributes_under_condition(attributes_condition_2, subject_data, i, "02")


def make_emg_area_under_curve_on_different_activities_plots(subject_data: MurderWallDetective):
    def create_label(trial: MurderWallAsset) -> str:
        return f"C{trial.metadata.condition}"

    def make_plot_for_certain_muscle(subject_data: MurderWallDetective, condition_data: pd.DataFrame, condition_id: str):
        for muscle in [f"{column}_C{condition_id}" for column in subject_data.get_columns()[3:]]:
            merged_data = pd.DataFrame({f"Activity {subject_data.get_activity_id(2 * i)}": frame[muscle] for i, frame in enumerate(condition_data)})
            plot_chunk(
                data_frame=merged_data,
                colors=["#984ea3"],
                labels=[],
                plotters=[make_boxplot, make_boxplot],
                title=f"Muscle {muscle[:-4]} | Condition {condition_id}",
                x_label="Activity",
                save_as=f"../test_data/plot_2/{muscle}",
                save_in_formats=["png", "pdf"],
                sub_group_length=1,
                show_legend=False,
                label_maker=lambda x: x
            )

    condition_1_values, condition_2_values = (
        WorkingData([activity for activity in subject_data.get_clipped_activity_pairs()])
        .map(lambda conditions: (compute_area_under_curve(conditions[0], create_label), compute_area_under_curve(conditions[1], create_label)))
        .unzip()
    )
    make_plot_for_certain_muscle(subject_data, condition_1_values.to_list(), "01")
    make_plot_for_certain_muscle(subject_data, condition_2_values.to_list(), "02")


def make_emg_area_under_curve_on_different_conditions_plots(subject_data: MurderWallDetective):
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

    for i, conditions in enumerate(subject_data.get_clipped_activity_pairs()):
        condition_1, condition_2 = conditions
        area_under_curve_condition_1 = compute_area_under_curve(condition_1, create_label)
        area_under_curve_condition_2 = compute_area_under_curve(condition_2, create_label)
        merged_data = merge_data_frames(WorkingData([area_under_curve_condition_1, area_under_curve_condition_2]))
        plot_chunk(
            data_frame=merged_data,
            colors=["#984ea3", "#ff7f00"],
            labels=["Condition A", "Condition B"],
            plotters=[make_boxplot, make_boxplot],
            title=rename_plot_title(subject_data.get_activity_id(2 * i)),
            x_label="Muscle",
            save_as=f"../test_data/plot_1/activity_{subject_data.get_activity_id(2 * i)}",
            save_in_formats=["png", "pdf"],
            sub_group_length=2,
            show_legend=True,
            label_maker=lambda x: x[:2]
        )


def main():
    '''
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
    '''

    # Evan's code --------------------------------------------------
    dataRelease.generateExemplar()
    expSetupFigures.generatePaperFigures()


if __name__ == "__main__":
    main()
