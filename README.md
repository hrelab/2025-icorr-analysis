# icorr-analysis

Creates plots using the data collected for icorr-2025

# Setting Up Environment

Run the following commands based on the state of your project.

## If you have pre-existing python virtual python environment

1. Activate the environment :)

2. Run `python -m pip install -e .` and the pyproject.toml will handle dependencies for you.

## If you do not have a pre-existing python virtual environment

1. Create the env `python -m venv .venv`

2. Source the env `source .venv/bin/activate`

3. Run `python -m pip install -e .` and the pyproject.toml will handle dependencies for you.

# Generating Plots

1. Make sure that you have the pre-processed data.

2. Make sure to have followed the virtual environment setup from above.

3. In the root of the project, run `python main.py`
