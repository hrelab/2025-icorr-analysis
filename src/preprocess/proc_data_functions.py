import os
import pandas as pd
import numpy as np
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Process window size and standard deviation multiplier.")
    
    # Add arguments
    parser.add_argument(
        '--window',
        type=int,
        default=400,
        help="The size of the rolling window (integer)."
    )
    parser.add_argument(
        '--sd_mult',
        type=int,
        default=4,
        help="The standard deviation multiplier (integer)."
    )
    
    # Parse the arguments
    args = parser.parse_args()
    return args

def grabData(partNum, cond, act):
    '''
        Gets and process all the data for a given participant, condition, and activity combination
    '''
    # Pull in all the data for the given combination (first try revision 2, then 1)
    try:
        emgData = pd.read_csv(f"raw_data/emg/rosbag-data-{partNum}-{cond}-{act}-02_0_emg.csv")
        gameData = pd.read_csv(f"raw_data/game/rosbag-data-{partNum}-{cond}-{act}-02_0_game.csv")
        forceData = pd.read_csv(f"raw_data/force/rosbag-data-{partNum}-{cond}-{act}-02_0_force.csv")
    except:
        emgData = pd.read_csv(f"raw_data/emg/rosbag-data-{partNum}-{cond}-{act}-01_0_emg.csv")
        gameData = pd.read_csv(f"raw_data/game/rosbag-data-{partNum}-{cond}-{act}-01_0_game.csv")
        forceData = pd.read_csv(f"raw_data/force/rosbag-data-{partNum}-{cond}-{act}-01_0_force.csv")

    return emgData, gameData, forceData

def getGameEnd(gameData : pd.DataFrame, maxTime):
    '''
        Find the end of the game when the red ball stops moving, not when the level is exited
    '''
    # Get the index of the the previous max time (when the level is exited)
    finalIndex = gameData.where(gameData["Ros Timestamp (ms)"] == maxTime).dropna().index.max()

    # Go through each time step of the game backwards
    for x in range(finalIndex-1, 0, -1):
        # Get the current position of the red ball and the next position
        posX, posY, posZ = gameData.iloc[x]["Tracker x"], gameData.iloc[x]["Tracker y"], gameData.iloc[x]["Tracker z"]
        posnX, posnY, posnZ = gameData.iloc[x+1]["Tracker x"], gameData.iloc[x+1]["Tracker y"], gameData.iloc[x+1]["Tracker z"]

        # If they are not the same, we found the last frame the ball is moving and the timestamp assosiated
        if posnX != posX or posnY != posY or posnZ != posZ:
            return gameData.iloc[x+1]["Ros Timestamp (ms)"]
        
    # Safeguard if it doesn't work...but should never get here
    return ValueError("No max game time found")

def getMinMaxTime(gameData):
    '''
        Gets the start of the game (when the countdown ends) and the end of the game
        when the red ball stops moving (meaning all activities have the same length)
    '''
    # Get the min and max times from the game (when the countdown ends to when exiting the level)
    minTime = gameData.min()['Ros Timestamp (ms)']
    maxTime = gameData.max()['Ros Timestamp (ms)']

    # Set the maxTime to when the red ball stops moving
    maxTime = getGameEnd(gameData, maxTime)

    return minTime, maxTime

def getIndecies(data, minTime, maxTime):
    '''
        Get the indecies of the start and stop times of the game to apply to other datasets
    '''
    # First try (ns) (for emgData) and then (ms) (for forceData)
    try:
        filt_ind = data.where((data["Ros Timestamp (ns)"] >= minTime) & (data["Ros Timestamp (ns)"] <= maxTime))
    except:
        filt_ind = data.where((data["Ros Timestamp (ms)"] >= minTime) & (data["Ros Timestamp (ms)"] <= maxTime))

    filt_ind = filt_ind.dropna().index
    startIndex = filt_ind.min()
    endIndex = filt_ind.max()

    return startIndex, endIndex


def temporalClip(partNum="13", cond="02", act="06", window=400):
    # Pull in data and get the min and max time stamps
    emgData, gameData, forceData = grabData(partNum, cond, act)
    minTime, maxTime = getMinMaxTime(gameData)
    
    # Find the indicies of the min and max time for EMG and Force
    startIndexEMG, endIndexEMG = getIndecies(emgData, minTime, maxTime)
    startIndexForce, endIndexForce = getIndecies(forceData, minTime, maxTime)

    # Just in case data needs extra offset for RMS to work with window (shouldn't occur)
    offset = 0
    if startIndexEMG < 400:
        offset = 400 - startIndexEMG
        emgData = pd.concat([emgData[:offset], emgData], axis=0)
        startIndexEMG += offset

    temp_emgData = emgData[startIndexEMG-window:endIndexEMG+offset]
    temp_forceData = forceData[startIndexForce:endIndexForce]
    
    # Return the processed emg and force data
    return temp_emgData, temp_forceData, gameData
