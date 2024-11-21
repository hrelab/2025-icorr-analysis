from murder_wall.MurderWall import MurderWall
from murder_wall.MurderWallDetective import MurderWallDetective
from analysis_tools.PatientDataExtractor import get_subjects
from analysis_tools.AreaUnderCurvePlottingUtilities import compute_area_under_curve_plot_for_activity, merge_area_under_curve_plots, plot_and_save


def make_emg_area_under_curve_plots(subject_data):
    for i, conditions in enumerate(subject_data.get_clipped_activity_pairs()):
        condition_1, condition_2 = conditions
        area_under_curve_condition_1 = compute_area_under_curve_plot_for_activity(condition_1)
        area_under_curve_condition_2 = compute_area_under_curve_plot_for_activity(condition_2)
        merged_data = merge_area_under_curve_plots(area_under_curve_condition_1, area_under_curve_condition_2)
        merged_data.to_csv(f"../test_data/{subject_data.get_activity_id(i)}.csv")
        plot_and_save(merged_data, subject_data.get_activity_id(i))


def main():
    murder_wall: MurderWall = MurderWall(get_subjects("../proc_data"))
    subject_data: MurderWallDetective = murder_wall.create_layout()
    make_emg_area_under_curve_plots(subject_data)


if __name__ == "__main__":
    main()
