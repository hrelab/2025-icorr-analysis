from experimental_setup_plots.util.showPlots import showPlots
from experimental_setup_plots.util.showPlots import showPlotsProcessed
import matplotlib.pyplot as plt
import os

def generateExemplar():
    sp = showPlotsProcessed()

    sp.pl.sharex = True

    # Expects a folder named 'subjects' in relative directory
    # Saves folder in 'subjects' folder, named 'figures'
    sp.initializeData()
    sp.makeAllSubjectFigures()

