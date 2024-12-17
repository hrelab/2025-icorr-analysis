from experimental_setup_plots.util.fileRead import fileReader
from experimental_setup_plots.util.plots import plotGenerator
import os
'''
    Utilizes plots class to generate figure(s) for subjects
    Works with raw, unproccesed data.
'''
class showPlots():

    def __init__(self):
        self.fr = fileReader()

        # Initialize plot generator and insert data
        self.pl = plotGenerator()
        self.pl.activityOrder = ['x-axis', 'y-axis', 'z-axis', 'torque', 'CW Circle', 'CCW Circle', 'XY 1', 'XY 2']
        self.pl.sharex = False

        # Subject id, gender, age, domininant hand
        self.demographicDict = {
            "03" : ["M", "23", "Right"],
            "06" : ["M", "23", "Right"],
            "04" : ["M", "22", "Left"],
            "15" : ["M", "27", "Left"],
            "09" : ["F", "23", "Right"],
            "05" : ["M", "22", "Right"],
            "19" : ["F", "70", "Left"],
            "20" : ["F", "46", "Right"],
            "02" : ["M", "20", "Left"],
            "14" : ["F", "21", "Right"],
            "01" : ["M", "33", "Left"],
            "07" : ["F", "31", "Right"],
            "12" : ["M", "22", "Right"],
            "13" : ["F", "29", "Right"],
            "08" : ["M", "28", "Right"],
            "21" : ["F", "24", "RightI"]

        }
    def initializeData(self):

        # Center directory to subjects, which holds all subject folders
        currPath = os.path.join('.', 'subjects')
        dir_list = os.listdir(currPath)
        for subject in dir_list: # Example: 03
            self.initializeSubject(subject)
   
    def initializeSubject(self, subject):
        # Still in 'subjects' directory, folderPath says which subject folder to use
        folderPath = os.path.join('.', 'subjects', subject)
        print(f"Initializing{subject}")
        dir_list = os.listdir(folderPath)

        # Should be 16, one folder for each activity
        for i in range(len(dir_list)):
            folderName = os.path.join(folderPath, dir_list[i])

            # Not the csv folder
            if (not folderName.endswith('_0')):
                continue

            # Splits folder name into its parameters (info[3] is the condition, info[4] is the activity)
            info = folderName.split('-')
            cond = int(info[3])
            act = int(info[4])

            for fileName in os.listdir(folderName):
                joined = os.path.join(folderName, fileName)
                self.fr.readFile(joined)
                if (fileName.endswith('emg.csv')):
                    self.pl.initializeEmg(subject, cond-1, act-1, self.fr.data)
                elif (fileName.endswith('force.csv')):
                    self.pl.initializeForce(subject, cond-1, act-1, self.fr.data)

                elif (fileName.endswith('game.csv')):
                    self.pl.initializeGame(subject, cond-1, act-1, self.fr.data)

    def makeAllSubjectFigures(self):

        currPath = os.path.join('.', 'subjects')

        path = os.path.join(currPath, 'figures')
        if not os.path.exists(path):
            os.mkdir(path) # Makes 'figures' folder within subjects folder

        dir_list = os.listdir(currPath)
        for folderName in dir_list: # Example: 03
            if (folderName == 'figures'):
                continue
            self.subjectFigures(folderName)

    # Given a subject, will create figures for entire activity
    def subjectFigures(self, subject):

        # Go inside 'figures' folder to make folder for figures of a subject
        currPath = os.path.join('.', 'subjects', 'figures', f"{subject}_figures")
        os.mkdir(currPath)

        subjectDems = self.demographicDict[subject]
        gender = subjectDems[0]
        age = subjectDems[1]
        hand = subjectDems[2]

        # Should be 2, one for each condition
        for i in range(2):
            for j in range(8):
                self.pl.rmsAndForce(currPath, subject, gender, age, hand, i + 1, j + 1)

'''
    Utilizes plots class to generate figure(s) for subjects
    Works with proccesed data.
'''
class showPlotsProcessed():

    def __init__(self):
        self.fr = fileReader()

        # Initialize plot generator and insert data
        self.pl = plotGenerator()
        self.pl.activityOrder = ['x-axis', 'y-axis', 'z-axis', 'torque', 'CW Circle', 'CCW Circle', 'XY 1', 'XY 2']
        self.pl.sharex = True

        # Subject id, gender, age, domininant hand
        self.demographicDict = {
            "03" : ["M", "23", "Right"],
            "06" : ["M", "23", "Right"],
            "04" : ["M", "22", "Left"],
            "15" : ["M", "27", "Left"],
            "09" : ["F", "23", "Right"],
            "05" : ["M", "22", "Right"],
            "19" : ["F", "70", "Left"],
            "20" : ["F", "46", "Right"],
            "02" : ["M", "20", "Left"],
            "14" : ["F", "21", "Right"],
            "01" : ["M", "33", "Left"],
            "07" : ["F", "31", "Right"],
            "12" : ["M", "22", "Right"],
            "13" : ["F", "29", "Right"],
            "08" : ["M", "28", "Right"],
            "21" : ["F", "24", "RightI"],
            "22" : ["M", "34", "LeftI"]

        }
    def initializeData(self):

        # Center directory to subjects, which holds all subject folders
        currPath = os.path.join('.', 'processed_data')

        dir_list = os.listdir(currPath)
        for subject in dir_list: # Example: 03
            self.initializeSubject(subject)

    def initializeSubject(self, subject):
        # Still in 'subjects' directory, folderPath says which subject folder to use
        folderPath = os.path.join('.', 'processed_data', subject)
        print(f"Initializing{subject}")
        # One folder for each condition
        for cond in ["01", "02"]:
            folderName = os.path.join(folderPath, cond)

            for fileName in os.listdir(folderName):
                joined = os.path.join(folderName, fileName)
                self.fr.readFile(joined)

                activity = int(fileName.split('-')[2][:2])-1

                if (fileName.__contains__('emg')):
                    self.pl.initializeEmgProcessed(subject, int(cond)-1, activity, self.fr.data)
                elif (fileName.__contains__('force')):
                    self.pl.initializeForceProcessed(subject, int(cond)-1, activity, self.fr.data)

    def makeAllSubjectFigures(self):

        currPath = os.path.join('.','processed_data')

        path = os.path.join(currPath, 'figures')
        if not os.path.exists(path):
            os.mkdir(path)

        folderPath = 'y'
        while folderPath != 'q':

            # Example: 03
            folderPath = input('Enter subject number: ')

            if (folderPath == 'q'):
                break
            elif (folderPath == 'all'):

                dir_list = os.listdir(currPath)
                for folderName in dir_list: # Example: 03
                    if (folderName == 'figures'):
                        continue
                    self.subjectFigures(folderName)

            else:
                self.subjectFigures(folderPath)

    # Given a subject, will create figures for entire activity
    def subjectFigures(self, subject):

        # Go inside 'figures' folder to make folder for figures of a subject
        currPath = os.path.join('.', 'processed_data', 'figures', f"{subject}_figures")
        os.mkdir(currPath)

        subjectDems = self.demographicDict[subject]
        gender = subjectDems[0]
        age = subjectDems[1]
        hand = subjectDems[2]

        # Should be 2, one for each condition
        for i in range(2):
            for j in range(8):
                self.pl.rmsAndForce(currPath, subject, gender, age, hand, i + 1, j + 1)
