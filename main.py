from murder_wall.MurderWall import MurderWall
from murder_wall.MurderWallDetective import MurderWallDetective
from analysis_tools.PatientDataExtractor import get_subjects
from analysis_tools.AreaUnderCurvePlottingUtilities import compute_area_under_curve_plot_for_activity, merge_area_under_curve_plots, plot_and_save
import pandas as pd


def make_plot_for_certain_muscle(subject_data, condition_data, condition_id):
    for muscle in [f"{column}_C{condition_id}" for column in subject_data.get_columns()[3:]]:
        merged_data = pd.DataFrame({f"Activity {subject_data.get_activity_id(2 * i)}": frame[muscle] for i, frame in enumerate(condition_data)})
        merged_data.to_csv(f"../test_data/plot_2/{muscle}.csv")
        plot_and_save(merged_data, f"Muscle {muscle} | Condition {condition_id}", f"../test_data/plot_2/{muscle}", "Activity")


def make_emg_area_under_curve_on_different_activities_plots(subject_data):
    condition_1_values = []
    condition_2_values = []
    for conditions in subject_data.get_clipped_activity_pairs():
        condition_1, condition_2 = conditions
        area_under_curve_condition_1 = compute_area_under_curve_plot_for_activity(condition_1)
        area_under_curve_condition_2 = compute_area_under_curve_plot_for_activity(condition_2)
        condition_1_values.append(area_under_curve_condition_1)
        condition_2_values.append(area_under_curve_condition_2)
    make_plot_for_certain_muscle(subject_data, condition_1_values, "01")
    make_plot_for_certain_muscle(subject_data, condition_2_values, "02")


def make_emg_area_under_curve_on_different_conditions_plots(subject_data):
    for i, conditions in enumerate(subject_data.get_clipped_activity_pairs()):
        condition_1, condition_2 = conditions
        area_under_curve_condition_1 = compute_area_under_curve_plot_for_activity(condition_1)
        area_under_curve_condition_2 = compute_area_under_curve_plot_for_activity(condition_2)
        merged_data = merge_area_under_curve_plots(area_under_curve_condition_1, area_under_curve_condition_2)
        merged_data.to_csv(f"../test_data/plot_1/activity_{subject_data.get_activity_id(2 * i)}.csv")
        plot_and_save(merged_data, f"Activity {subject_data.get_activity_id(2 * i)}", f"../test_data/plot_1/activity_{subject_data.get_activity_id(2 * i)}", "Muscles (Condition 1, Condition 2)")


def main():
    murder_wall: MurderWall = MurderWall(get_subjects("../proc_data"))
    subject_data: MurderWallDetective = murder_wall.create_layout()
    make_emg_area_under_curve_on_different_conditions_plots(subject_data)
    make_emg_area_under_curve_on_different_activities_plots(subject_data)


if __name__ == "__main__":
    main()
