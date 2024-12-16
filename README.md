# Analysis Code: An Extensible Platform for Measurement and Modification of Muscle Engagement During Upper-Limb Robot-Facilitated Rehabilitation (ICORR 2025)

## Overview

This folder contains the analysis code associated with the paper titled ***"An Extensible Platform for Measurement and Modification of Muscle Engagement During Upper-Limb Robot-Facilitated Rehabilitation"*** submitted to the 2025 IEEE International Conference on Rehabilitation Robotics (ICORR). Code can be used alongside the [released data set]([url](https://tinyurl.com/hrelab-2025-icorr)) to generate all associated publication plots and statistical analyses.

## License

The data, documentation and associated code is provided as-is; however, we invite anyone who wishes to adapt and use it under a Creative Commons Attribution 4.0 International License. Please cite the following publication if you use this code or data in your research:

```bibtex
@inproceedings{AnandRehabPlatform2025,
  title={An Extensible Platform for Measurement and Modification of Muscle Engagement During Upper-Limb Robot-Facilitated Rehabilitation},
  booktitle = {9th IEEE/RAS-EMBS International Conference on Rehabilitation Robotics ({ICORR})},
  author = {Ajay Anand and Chad A. Berghoff and Carson J. Wynn and Evan Cole Falconer and Gabriel Parra and Jono Jenkens and 
  Caleb J. Thomson and W. Caden Hamrick and Jacob A. George and Laura A. Hallock},
  date = {},
  year = {2025},
  pages={},
  isnn ={},
  doi = {},
  ourl = {},
  urldate = {},
  abstract = {},
  eventtitle = {9th IEEE/RAS-EMBS International Conference on Rehabilitation Robotics ({ICORR})},
  keywords = {rehabilitation robotics, human–robot interaction, biomechanics, surface electromyography (sEMG), user-centered design}
}
```
## Installation

### Downloading the Code and Data

To Download all modules and scripts, clone the repository via

```bash
git clone git@github.com:hrelab/2025-icorr-analysis.git
```

or download and extract the repository ZIP file. 

Next, download the `processed_data` folder from the [released data set]([url](https://tinyurl.com/hrelab-2025-icorr)) and place it in the top-level directory. (Due to GDrive's upload limits, this may require downloading, extracting, and re-merging the folder file tree.)

This will result in the following project structure:

```
2025-icorr-analysis/
├── LICENSE
├── main.py
├── processed_data/
├── pyproject.toml
├── README.md
├── src/
└── tests/
```

### Setting Up Environment and Dependencies

We recommend running this code inside a Python virtual environment via the following commands. From the `2025-icorr-analysis` folder, run:

```bash
python -m venv .venv
```

to create a virtual environment, and then source it via

```bash
source .venv/bin/activate # you may need to modify this command for non-Unix (i.e., Windows) systems
```

Once you've sourced your virtual environment successfully (as indicated by `which python` pointing inside your new `.venv` folder and/or `(.venv)` prepending your command line), install all dependencies from `pyproject.toml` via

```bash
python -m pip install -e .
```

## Usage

Once the file tree and dependencies are set up as specified above, run (from the base `2025-icorr-analysis` directory):

```bash
python main.py --generate_plots
```

to generate all plots and write them to the (new, unless previously generated) `processed_data_plots` directory.


## Work In Progress Features

We are currently augmenting the code above with additional tools to allow manipulation and display of individual time-series data trials, both raw and processed. Check back soon for additional functionality, or contact <ajay.anand@utah.edu> and <laura.hallock@utah.edu> for a status update.

<!-- These features are in current development and will not work.

### Running the whole pipeline

1. Make sure that you have the unprocessed data.

2. Make sure to have followed the virtual environment setup from above.

3. In the root of the project, run `python main.py --process_data --generate_plots --generate_exemplar`

### Running the data processer on the unprocessed data

1. Make sure that you have the unprocessed data.

2. Make sure to have followed the virtual environment setup from above.

3. In the root of the project, run `python main.py --process_data`

### Generating Exemplar Plots

1. Make sure that you have the processed data.

2. Make sure to have followed the virtual environment setup from above.

3. In the root of the project, run `python main.py --generate_exemplar` -->
