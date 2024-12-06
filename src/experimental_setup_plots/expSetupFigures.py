from src.experimental_setup_plots.util.showPlots import showPlots
import matplotlib.pyplot as plt
import os

# Generates the "Experiment Setup" figures as seen on the paper
#   - EMG for subject 7, condition A, activity 2
def generatePaperFigures():
    sp = showPlots()

    # Parameters to remove borders on plots
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.spines.bottom'] = False
    plt.rcParams['axes.spines.left'] = False

    sp.pl.sharex = False

    subject = '07'
    cond = 0
    activity = 1

    os.chdir('subjects')
    sp.initializeSubject(subject)
    
    sp.pl.rmsOverRaw(plt.figure(), subject, cond, activity)
    sp.pl.overlayedForce(plt.figure(), subject, cond, activity)

    sp.pl.showPlots()

