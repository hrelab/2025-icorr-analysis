# 2025-icorr-analysis

Creates plots using the data collected for icorr-2025

The code and documentation are provided as-is; however, we invite anyone who wishes to adapt and use it under a Creative Commons Attribution 4.0 International License. We would appreciate it if you could cite the following publication if you use this code or data in your research:

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

## Setting Up File Structure

When you clone this repository from github your project structure will look like this:

```
2025-icorr-analysis/
├── LICENSE
├── main.py
├── pyproject.toml
├── README.md
├── src/
├── subjects/
└── tests/
```

To ensure that the script runs correctly, the following data needs to be downloaded and moved into this directory.

1. processed_data
2. unprocessed_data

You can download this data from the following link: [2025 ICORR Data](<https://drive.google.com/drive/u/0/folders/1n4cooQM1GK94jVku2kTv6BuAmHD2BzN7>)

Both pieces of data can be moved into the 2025-icorr-analysis directory, sitting along side the main.py and src directory.

When you have moved all of the data into this directory, your project structure should look like this:

```
2025-icorr-analysis/
├── LICENSE
├── main.py
├── pyproject.toml
├── pyproject.toml
├── README.md
├── processed_data
├── unprocessed_data
├── src/
├── subjects/
└── tests/
```

## Setting Up Environment

Run the following commands based on the state of your project.

### If you have pre-existing python virtual python environment

1. Activate the environment :)

2. Run `python -m pip install -e .` and the pyproject.toml will handle dependencies for you.

### If you do not have a pre-existing python virtual environment

1. Create the env `python -m venv .venv`

2. Source the env `source .venv/bin/activate`

3. Run `python -m pip install -e .` and the pyproject.toml will handle dependencies for you.

## Generating Plots

1. Make sure that you have the processed data.

2. Make sure to have followed the virtual environment setup from above.

3. In the root of the project, run `python main.py --generate_plots`

4. The generated plots are now stored in the `processed_data_plots` directory

## Work In Progress Features

These features are in current development and will not work.

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

3. In the root of the project, run `python main.py --generate_exemplar`
