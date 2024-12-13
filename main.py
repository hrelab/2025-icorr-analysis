from src.murder_wall.murderwall import MurderWall
from src.murder_wall.murderwall_detective import MurderWallDetective
from src.analysis_tools.patient_data_extractor import get_subjects
from src.analysis_tools.plot_3 import make_plot_3
from src.analysis_tools.plot_1 import make_plot_1
from src.analysis_tools.plot_2 import make_plot_2
import src.analysis_tools.plot_2_paper_version as p2pv
from src.murder_wall.experiment_parameters import ExperimentParameters
from os.path import join
from src.experimental_setup_plots import (
    expSetupFigures,
    dataRelease
)
import os
from argparse import ArgumentParser
from src.preprocess.proc_data_main import process_data


def create_needed_directories():
    if not os.path.exists(join(".", "proc_data")):
        print("Processed data not found. Follow the README to ensure the script can find the processed data.")
    if not os.path.exists(join(".", "processed_data_plots")):
        os.mkdir(join(".", "processed_data_plots"))
    if not os.path.exists(join(".", "processed_data_plots", "plot_1")):
        os.mkdir(join(".", "processed_data_plots", "plot_1"))
    if not os.path.exists(join(".", "processed_data_plots", "plot_2")):
        os.mkdir(join(".", "processed_data_plots", "plot_2"))
    if not os.path.exists(join(".", "processed_data_plots", "plot_3")):
        os.mkdir(join(".", "processed_data_plots", "plot_3"))
    if not os.path.exists(join(".", "subjects")):
        os.mkdir(join(".", "subjects"))
        for subject in get_subjects(join(".", "proc_data")):
            os.mkdir(join(".", "subjects", subject))


def main():
    create_needed_directories()
    argument_parser = ArgumentParser("Run Plot Generator | Preprocess Data | Generate Exemplar Plots")
    argument_parser.add_argument("--generate_plots", action="store_true")
    argument_parser.add_argument("--preprocess", action="store_true")
    argument_parser.add_argument("--generate_exemplar", action="store_true")
    argument_parser.add_argument(
        '--window',
        type=int,
        default=400,
        help="The size of the rolling window (integer)."
    )
    argument_parser.add_argument(
        '--sd_mult',
        type=int,
        default=4,
        help="The standard deviation multiplier (integer)."
    )
    arguments = argument_parser.parse_args()

    if arguments.preprocess:
        process_data(arguments)

    if arguments.generate_exemplar:
        dataRelease.generateExemplar()
        expSetupFigures.generatePaperFigures()

    if arguments.generate_plots:
        experiment_parameters: ExperimentParameters = ExperimentParameters(
            activities=[f"0{n}" for n in range(1, 9)],
            conditions=["01", "02"],
            subjects=get_subjects(join(".", "processed_data")),
            data_types=["emg", "force"]
        )
        murder_wall: MurderWall = MurderWall(experiment_parameters)
        subject_data: MurderWallDetective = murder_wall.create_layout()
        make_plot_1(subject_data)
        make_plot_2(subject_data)
        p2pv.make_plot_2(subject_data)
        make_plot_3(subject_data)


if __name__ == "__main__":
    main()
