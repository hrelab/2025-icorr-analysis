from murder_wall.MurderWall import MurderWall
from murder_wall.MurderWallDetective import MurderWallDetective
from analysis_tools.PatientDataExtractor import get_subjects
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain


def plot_and_save(area_under_curve_data: pd.DataFrame, activity_id: str):
    plt.figure(figsize=(40, 15))
    area_under_curve_data.boxplot(showfliers=False)
    plt.title(f"Activity {activity_id}")
    plt.savefig(f"../test_data/activity_{activity_id}.png")
    plt.close()


def compute_area_under_curve_plot_for_activity(subject_data: MurderWallDetective, index: int) -> pd.DataFrame:
    condition_id = subject_data.get_activity(index)[0].metadata.condition
    columns = subject_data.get_columns()[3:]
    area_under_curve_data_frame = pd.DataFrame(columns=columns)
    for subject_doing_activity in subject_data.get_activity(index):
        subject_emg_activity = subject_doing_activity.get_emg_frame().iloc[:, 3:]
        area_under_curve = subject_emg_activity.cumsum()
        if len(area_under_curve) < 1:
            continue
        area_under_curve_data_frame.loc[len(area_under_curve_data_frame)] = area_under_curve.iloc[-1]
    columns_with_condition = [f"{column}_C{condition_id}" for column in columns]
    rename_map = dict(zip(columns, columns_with_condition))
    area_under_curve_data_frame = area_under_curve_data_frame.rename(columns=rename_map)
    return area_under_curve_data_frame


def merge_area_under_curve_plots(auc_condition_1: pd.DataFrame, auc_condition_2: pd.DataFrame) -> pd.DataFrame:  # aoc = area under curve
    columns_condition_1 = auc_condition_1.columns.tolist()
    columns_condition_2 = auc_condition_2.columns.tolist()
    merged_columns = list(chain.from_iterable(zip(columns_condition_1, columns_condition_2)))
    merged_tables = pd.concat([auc_condition_1, auc_condition_2], axis=1)
    merged_tables = merged_tables[merged_columns]
    return merged_tables


def main():
    murder_wall: MurderWall = MurderWall(get_subjects("../proc_data"))
    subject_data: MurderWallDetective = murder_wall.create_layout()
    for i in range(0, subject_data.columns, 2):
        area_under_curve_condition_1 = compute_area_under_curve_plot_for_activity(subject_data, i)
        area_under_curve_condition_2 = compute_area_under_curve_plot_for_activity(subject_data, i + 1)
        merged_data = merge_area_under_curve_plots(area_under_curve_condition_1, area_under_curve_condition_2)
        merged_data.to_csv(f"../test_data/{subject_data.get_activity_id(i)}.csv")
        plot_and_save(merged_data, subject_data.get_activity_id(i))


if __name__ == "__main__":
    main()
