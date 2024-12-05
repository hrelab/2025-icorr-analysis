from src.murder_wall.murderwall_detective import MurderWallDetective
from src.murder_wall.murderwall_asset import MurderWallAsset
from src.analysis_tools.area_under_curve_plotting_utilities import (
    compute_area_under_curve
)
from src.gstd.working_data import WorkingData
from src.analysis_tools.plotting_utilities import plot_chunk, make_boxplot
import pandas as pd


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
            label_maker=lambda x: x,
        )


def create_label(trial: MurderWallAsset) -> str:
    return f"C{trial.metadata.condition}"


def make_plot_2(subject_data: MurderWallDetective):
    condition_1_values, condition_2_values = (
        WorkingData([activity for activity in subject_data.get_clipped_activity_pairs()])
        .map(lambda conditions: (compute_area_under_curve(conditions[0], create_label), compute_area_under_curve(conditions[1], create_label)))
        .unzip()
    )
    make_plot_for_certain_muscle(subject_data, condition_1_values.to_list(), "01")
    make_plot_for_certain_muscle(subject_data, condition_2_values.to_list(), "02")
