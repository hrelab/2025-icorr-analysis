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


def main():
    experiment_parameters: ExperimentParameters = ExperimentParameters(
        activities=[f"0{n}" for n in range(1, 9)],
        conditions=["01", "02"],
        subjects=get_subjects(join("..", "proc_data")),
        data_types=["emg", "force"]
    )

    murder_wall: MurderWall = MurderWall(experiment_parameters)
    subject_data: MurderWallDetective = murder_wall.create_layout()
    dataRelease.generateExemplar()
    expSetupFigures.generatePaperFigures()
    make_plot_1(subject_data)
    make_plot_2(subject_data)
    p2pv.make_plot_2(subject_data)
    make_plot_3(subject_data)


if __name__ == "__main__":
    main()
