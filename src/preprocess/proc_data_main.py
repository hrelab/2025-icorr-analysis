from proc_data_functions import *

'''
    This script takes in the raw data and does the following preprocessing:
    1) temporally clips to only have data during the game time (when red ball is moving)
    2) clips the emgData so outlier spikes in the emg are cut off (default: 4std away from mean)
    3) renames columns to shortened names
    4) returns the clipped EMG (temporally/amplitude) and Force (temporally) data and orginal Game data
        - all data is stored in the path "./proc_data/{participantID}/{conditionID}/processed-{emg/force/game}-{activityID}.csv"
        - data will be overwritten if path and files already exist
        - if path does not exist, it will create one
'''

# Demographics of subjects in trial
demographicDict = {
    "02" : ["M", "20", "L"],
    "03" : ["M", "23", "R"],
    "04" : ["M", "22", "L"],
    "05" : ["M", "22", "R"],
    "07" : ["F", "31", "R"],
    "08" : ["M", "28", "R"],
    "09" : ["F", "23", "R"],
    "12" : ["M", "22", "R"],
    "13" : ["F", "29", "R"],
    "14" : ["F", "21", "R"],
    "15" : ["M", "27", "R"],
    "19" : ["F", "70", "L"],
    "20" : ["F", "46", "R"],
    "21" : ["F", "24", "RI"],
    "22" : ["M", "34", "LI"]
}

# Get the arguments in the command line to use for more control over processing
args = parse_args()
window = args.window
sd_mult = args.sd_mult

# Create a high level dataFrame to hold all the data from all participants/conditions/activities
fullFrame = pd.DataFrame()

# Go through each of the participants in the demographics
for par in demographicDict.keys():
    # Save all the emgData per participant to clip later, and reset the dataFrame
    emgs = {}
    fullFrame = fullFrame.iloc[0:0]

    # Go through each condition and activity. Save the data
    # to the directory. If not exist, create the directory
    for con in ["01", "02"]:
        for x in range(1, 9):
            if not os.path.exists(f"proc_data/{par}/{con}/"):
                os.makedirs(f"proc_data/{par}/{con}")
            act = f"0{x}"

            # Clip the data temporally, run the RMS window, and then save the EMG to a temp to save for participant
            tempEMG, tempForce, tempGame = temporalClip(par, con, act)
            tempEMG.iloc[:, 3:] = tempEMG.iloc[:, 3:].rolling(window=window).apply(lambda x: np.sqrt(np.mean(x**2)), raw=True)
            emgs[(con, act)] = tempEMG[window:]

            # Save the force and game data
            tempForce.to_csv(f"proc_data/{par}/{con}/processed-force-{act}.csv")
            tempGame.to_csv(f"proc_data/{par}/{con}/processed-game-{act}.csv")
    
    # Back on the participant level, save the emgs and clip to (sd_mult*sd + mean)
    list_emg = [emgs[e] for e in emgs.keys()]
    fullFrame = pd.concat(list_emg, axis=0, ignore_index=True)
    mean = fullFrame.mean()[3:]
    sd = fullFrame.std()[3:]
    sd *= sd_mult

    # Saving normalized emg
    for e in emgs:
        temp = emgs[e]
        condition, activity = e

        # Clip and normalize data
        temp.iloc[:,3:] = temp.iloc[:, 3:].clip(axis=1, upper=(mean + sd))
        temp.iloc[:, 3:] = temp.iloc[:, 3:].div(mean+sd)

        # Rename column names to abbreviated versions
        names = {}
        newn = ["BB", "PD", "AD", "MD", "TR", "FL", "EX", "BR"]
        for i, x in enumerate(temp.keys()[3:]):
            names[x] = newn[i]
        temp.rename(columns = names, inplace = True)

        # Save the EMG data
        temp.to_csv(f"proc_data/{par}/{condition}/processed-emg-{activity}.csv")