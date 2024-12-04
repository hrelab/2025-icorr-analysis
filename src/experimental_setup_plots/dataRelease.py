import util.showPlots as showPlots
import matplotlib.pyplot as plt
import os

def generateExemplar():
    sp = showPlots.showPlots()

    sp.pl.sharex = True

    # Expects a folder named 'subjects' in relative directory
    # Saves folder in 'subjects' folder, named 'figures'
    sp.initializeData()
    sp.makeAllSubjectFigures()

