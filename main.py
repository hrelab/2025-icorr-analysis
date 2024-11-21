from murder_wall.MurderWall import MurderWall
from murder_wall.MurderWallDetective import MurderWallDetective
from analysis_tools.PatientDataExtractor import get_subjects
import pandas as pd
import matplotlib.pyplot as plt


def plot_and_save(area_under_curve_data, activity_id, condition_id):
    plt.figure(figsize=(20, 10))
    area_under_curve_data.boxplot(showfliers=False)
    plt.title(f"Activity {activity_id} | Condition {condition_id}")
    plt.savefig(f"../test_data/activity_{activity_id}-condition_{condition_id}.png")
    plt.close()


def compute_area_under_curve_plot_for_activity(subject_data: MurderWallDetective, index: int):
    area_under_curve_data_frame = pd.DataFrame(columns=subject_data.get_columns())
    activity_id = subject_data.get_activity(index)[0].metadata.activity
    condition_id = subject_data.get_activity(index)[0].metadata.condition
    for subject_doing_activity in subject_data.get_activity(index):
        area_under_curve = subject_doing_activity.get_emg_frame().cumsum()
        area_under_curve_data_frame.loc[len(area_under_curve_data_frame)] = area_under_curve.iloc[-1]
    plot_and_save(area_under_curve_data_frame, activity_id, condition_id)


def main():
    murder_wall: MurderWall = MurderWall(get_subjects("../proc_data"))
    subject_data: MurderWallDetective = murder_wall.create_layout()
    for i in range(0, subject_data.columns, 2):
        compute_area_under_curve_plot_for_activity(subject_data, i)
        compute_area_under_curve_plot_for_activity(subject_data, i + 1)


if __name__ == "__main__":
    main()
