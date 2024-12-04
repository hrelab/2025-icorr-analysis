from experimental_setup_plots.util.showPlots import showPlots
import matplotlib.pyplot as plt
import os

def generateExemplar():
    sp = showPlots()

    sp.pl.sharex = True

    # Expects a folder named 'subjects' in relative directory
    # Saves folder in 'subjects' folder, named 'figures'
    sp.initializeData()
    sp.makeAllSubjectFigures()

