import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import os

''' Class that parses, organizes, and stores EMG data along with timestamp if included.
    Contains classes that create different plots:
        - some require input
        - some utilize standard emg data stored in class
    Make sure to always use showPlots() at the end of creating the plots to show them
'''
class plotGenerator():

    # Initialize arrays and variables to save space

    # 2 x 8 Array where each entry is a dictionary:
    #   Key is subject ID, value is : (emg_data, etimeStamp)
    subjectEmg = [[dict() for i in range(8)] for j in range(2)] 

    #   Key is subject ID, value is : ([fx, fy, fz, tx, ty, tz], ftimeStamp)
    subjectForce = [[dict() for i in range(8)] for j in range(2)] 

    #   Key is subject ID, value is : ([px, py, pz, trackx, tracky, trackz], gtimeStamp, score)
    subjectGame = [[dict() for i in range(8)] for j in range(2)] 


    # Emg fields
    channels = 0
    channelNames = [] # Same for each subject
    namesAbv = []
    samples = 400

    # Give the arrays names, same for each subject
    forceNames = []
    forceNamesAbv = ['x', 'y', 'z', 'tx', 'ty', 'tz']

    activityOrder = []

    sharex = False # Choose whether to show ticks for each graph

    # Plot settings
    plt.rcParams["savefig.format"] = 'pdf'
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams["xtick.labelsize"] = 10
    plt.rcParams["ytick.labelsize"] = 10

    fontPath = os.path.join('src', 'experimental_setup_plots', 'Open_Sans')

    for path in os.listdir(fontPath):
            if (path.endswith('.ttf')):
                path = os.path.join(fontPath, path)
                font_manager.fontManager.addfont(path)
    fontPath = os.path.join(fontPath, 'static')
    for path in os.listdir(fontPath):
            if (path.endswith('.ttf')):
                path = os.path.join(fontPath, path)
                font_manager.fontManager.addfont(path)
    plt.rcParams['font.family'] = 'Open Sans'
    
    emgRawColor = '#A6A6A6'
    #emgRawColor = '#5084b5'
    emgRmsColor = '#163E64'

    ftxColor = '#163E64'
    ftyColor = '#215F9A'
    ftzColor = '#4E95D9'

    #backplotColor = '#9A9CA1'
    backplotColor = '#f7f7f7'
    
    # Initializes all Emg data fields using the given numpy array read from file
    def initializeEmg(self, subject, cond, act, data):

        emg_data = data[1:, 3:].astype(float)

        etimeStamp = data[1:, 0].astype(float)
        etimeStamp = np.linspace(etimeStamp[0], etimeStamp[len(etimeStamp) - 10], len(emg_data[:,0])) # fill in gaps
        offset = etimeStamp[0]
        etimeStamp[:] -= offset # Normalize so time starts from 0
        etimeStamp[:] *=  1e-9 # Convert time stamp from nanoseconds to seconds

        self.channelNames = data[0, 3:]
        self.channels = len(self.channelNames)
        self.namesAbv = ['BB', 'PD', 'AD', 'MD', 'TR', 'FL', 'EX', 'BR']

        # Put into array
        self.subjectEmg[cond][act][subject] = (emg_data, etimeStamp)
    
    # Initializes all Force Sensor data fields using the given numpy array read from file
    def initializeForce(self, subject, cond, act, data):

        forceData = data[1:, 2:].astype(float)

        ftimeStamp = data[1:,0].astype(float)
        offset = ftimeStamp[0]
        ftimeStamp[:] -= offset # Normalize so time starts from 0
        ftimeStamp[:] *= 1e-9

        # Place forces in respective arrays
        fx = forceData[:, 0]
        fy = forceData[:, 1]
        fz = forceData[:, 2]

        # Place torques in respective arrays
        tx = forceData[:, 3]
        ty = forceData[:, 4]
        tz = forceData[:, 5]

        forces = [fx, fy, fz, tx, ty, tz]

        # Give the arrays names
        self.forceNames = data[0, 2:]
        self.forceNamesAbv = ['x', 'y', 'z', 'tx', 'ty', 'tz']

        # Put into array
        self.subjectForce[cond][act][subject] = (forces, ftimeStamp)
    
    # Initializes all Emg data fields using the given numpy array read from file
    def initializeEmgProcessed(self, subject, cond, act, data):

        emg_data = data[1:, 4:].astype(float)

        etimeStamp = data[1:, 1].astype(float)
        etimeStamp = np.linspace(etimeStamp[0], etimeStamp[len(etimeStamp) - 10], len(emg_data[:,0])) # fill in gaps

        offset = etimeStamp[0]
        etimeStamp[:] -= offset # Normalize so time starts from 0
        etimeStamp[:] *=  1e-9 # Convert time stamp from nanoseconds to seconds


        self.channelNames = data[0, 4:]
        self.channels = len(self.channelNames)
        self.namesAbv = ['BB', 'PD', 'AD', 'MD', 'TR', 'FL', 'EX', 'BR']

        # Put into array
        self.subjectEmg[cond][act][subject] = (emg_data, etimeStamp)
    
    # Initializes all Force Sensor data fields using the given numpy array read from file
    def initializeForceProcessed(self, subject, cond, act, data):

        forceData = data[1:, 3:].astype(float)

        ftimeStamp = data[1:,1].astype(float)
        offset = ftimeStamp[0]
        ftimeStamp[:] -= offset # Normalize so time starts from 0
        ftimeStamp[:] *= 1e-9

        # Place forces in respective arrays
        fx = forceData[:, 0]
        fy = forceData[:, 1]
        fz = forceData[:, 2]

        # Place torques in respective arrays
        tx = forceData[:, 3]
        ty = forceData[:, 4]
        tz = forceData[:, 5]

        forces = [fx, fy, fz, tx, ty, tz]

        # Give the arrays names
        self.forceNames = data[0, 3:]
        self.forceNamesAbv = ['x', 'y', 'z', 'tx', 'ty', 'tz']

        # Put into array
        self.subjectForce[cond][act][subject] = (forces, ftimeStamp)

    def initializeGame(self, subject, cond, act, data):
        
        gameData = data[1:, 2:].astype(float)

        gtimeStamp = data[1:, 0].astype(float)

        offset = gtimeStamp[0]
        gtimeStamp[:] -= offset
        gtimeStamp[:] *= 1e-9


        # Place player positions in respective arrays
        px = gameData[:, 0]
        py = gameData[:, 1]
        pz = gameData[:, 2]

        # Place tracker positions in respective arrays
        trackx = gameData[:, 3]
        tracky = gameData[:, 4]
        trackz = gameData[:, 5]

        # Get final score
        score = data[:, 1]

        positions = [px, py, pz, trackx, tracky, trackz]
        # Put into array
        self.subjectGame[cond][act][subject] = (positions, gtimeStamp, score)
    
    # Adjusts forces and torques by an offset, so they start at 0
    def normalizeForce(self, subject, cond, act):
        # Grab from array
        forces, ftimeStamp = self.subjectForce[cond][act][subject]
        
        # Loop through and subtract offset
        for i in range(len(forces)):
            offset = forces[i][0]

            forces[i] -= offset
    
    # Optional; If no names inserted, will initialized as above
    def nameChannels(self, names, abv):
        self.channelNames = names
        self.namesAbv = abv

    # EMG PLOTS ==============================================================================================
    # Creates a standard plot that displays EMG data for time x
    def timePlot(self, fig, subject, cond, activity):

        emg_data, etimeStamp = self.subjectEmg[cond][activity][subject]

        # Create figure and subplot; title, label x and y
        ax = fig.subplots(self.channels, 1)
        fig.suptitle('Time based EMG', fontsize = 16)
        fig.supxlabel('Time (s)', fontsize = 16)
        fig.supylabel('Voltage (mV)', fontsize = 16)

        # x-axis will be time stamp
        xaxis = etimeStamp

        # Plot each channel seperately
        for i in range(len(ax)):
            ax[i].set_title(self.channelNames[i], fontstyle='italic', fontsize = 10)
            ax[i].set_ylim(0, 2)
            ax[i].plot(xaxis, emg_data[:,i])
            # Turn off xticks for all plots except last
            if (i != len(ax)-1 and self.sharex):
                ax[i].set_xticklabels([])
        
        return ax
    
    # Create RMS smoothed plot of EMG data
    def rmsPlot(self, fig, subject, cond, activity):
        emg_data, etimeStamp = self.subjectEmg[cond][activity][subject]

        data = emg_data
        xaxis = etimeStamp

        # Create figure and subplot; title, label x and y
        ax = fig.subplots(len(data[0, :]), 1)
        fig.suptitle('RMS of EMG', fontsize = 10)
        fig.supxlabel('Time (s)', fontsize = 10)
        fig.supylabel('Voltage (mV)', fontsize = 10)

        # Initialize rms array to save space
        rmsData = np.zeros((len(data[:, 0]), len(ax)))

        # Plot each channel seperately, and store RMS data
        for i in range (len(ax)):
            rmsData[:,i] = self.__window_rms(data[:,i], self.samples)
            ax[i].plot(xaxis, rmsData[:,i], linewidth = 1)

            # Add in small box to label channel
            ax[i].annotate(self.namesAbv[i], xy=(0,1), xycoords = 'axes fraction',
                              xytext = (+0.5, -0.5), textcoords = 'offset fontsize',
                              fontsize = 'medium', verticalalignment = 'top', fontweight = 'bold')

            # Turn off xticks for all plots except last
            if (i != len(ax)-1 and self.sharex):
                ax[i].set_xticklabels([])

    # Creates a rms overlayed raw plot
    def rmsOverRaw(self, fig, subject, cond, activity):
        emg_data, etimeStamp = self.subjectEmg[cond][activity][subject]

        xaxis = etimeStamp
        raw = emg_data

        # Create figure and subplot; title, label x and y
        ax = fig.subplots(self.channels, 1)
        fig.subplots_adjust(top = .95, bottom = 0.1, hspace = 0.5)
        fig.suptitle('Raw and RMS', fontsize = 10)
        fig.supxlabel('Time (s)', fontsize = 10)
        fig.supylabel('Voltage (mV)', fontsize = 10)

        # Initialize rms array to save space
        rmsData = np.zeros((len(raw[:, 0]), len(ax)))

        # Plot each channel seperately, and store RMS data
        for i in range (len(ax)):
            ax[i].set_facecolor(self.backplotColor)
            rmsData[:,i] = self.__window_rms(raw[:,i], self.samples)

            ax[i].plot(xaxis, raw[:, i], linewidth = 0.5, color = self.emgRawColor, label = 'raw')
            ax[i].plot(xaxis, rmsData[:,i], linewidth = 2, color = self.emgRmsColor, label = 'rms')

            # Add in small box to label channel
            ax[i].annotate(self.namesAbv[i], xy=(0,1), xycoords = 'axes fraction',
                              xytext = (+0.5, -0.5), textcoords = 'offset fontsize',
                              fontsize = 'medium', verticalalignment = 'top', fontweight = 'bold')

            # Turn off xticks for all plots except last
            if (i != len(ax)-1 and self.sharex):
                ax[i].set_xticklabels([])

        ax[0].legend(bbox_to_anchor = (1, 0), bbox_transform = fig.transFigure, loc = "lower right", ncol = 2)
        return ax

    # Helper function that RMS envelopes over a given array
    def __window_rms(self, a, sample):

        window_size = sample
        a2 = np.power(a,2)
        window = np.ones(window_size)/float(window_size)

        return np.sqrt(np.convolve(a2, window, 'same'))
    
    # FORCE PLOTS ===========================================================================================
    # Returns axes of 6 channels of force plots. (XYZ Force and Torque)
    def forcePlot(self, fig, subject, cond, act):
        forces, ftime = self.subjectForce[cond][act][subject]

        # Create figure and subplot; title, label x and y
        ax = fig.subplots(len(forces), 1)
        fig.suptitle('Time based Force', fontsize = 10)
        fig.supxlabel('Time (s)', fontsize = 10)
        fig.supylabel('Force (lb)', fontsize = 10)

        # x-axis will be time stamp
        xaxis = ftime

        # Plot each channel seperately
        for i in range(len(ax)):
            ax[i].plot(xaxis, forces[i])

            # Add in small box to label channel
            ax[i].annotate(self.forceNamesAbv[i], xy=(0,1), xycoords = 'axes fraction',
                              xytext = (+0.5, -0.5), textcoords = 'offset fontsize',
                              fontsize = 'medium', verticalalignment = 'top', fontweight= 'bold'
                              )

            # Turn off xticks for all plots except last
            if (i != len(ax)-1 and self.sharex):
                ax[i].set_xticklabels([])
        
        return fig, ax
    
    def overlayedForce(self, fig, subject, cond, act):
        self.normalizeForce(subject, cond, act)

        forces, ftime = self.subjectForce[cond][act][subject]

        # Create 2 subplots, one for force and one for torque
        ax = fig.subplots(2, 1)

        fig.suptitle('Time based Force and Torque', fontsize = 10)
        fig.supxlabel('Time (s)', fontsize = 10)
        fig.supylabel('Force (lb)', fontsize = 10)

        # x-axis will be time stamp
        xaxis = ftime

        ax[0].set_facecolor(self.backplotColor)
        ax[1].set_facecolor(self.backplotColor)

        # Plot forces
        ax[0].plot(xaxis, forces[0], color = self.ftxColor, label = 'x')
        ax[0].plot(xaxis, forces[1], color = self.ftyColor, label = 'y')
        ax[0].plot(xaxis, forces[2], color = self.ftzColor, label = 'z')

        # Plot torques
        ax[1].plot(xaxis, forces[3], color = self.ftxColor)
        ax[1].plot(xaxis, forces[4], color = self.ftyColor)
        ax[1].plot(xaxis, forces[5], color = self.ftzColor)

        ax[0].legend(bbox_to_anchor = (1, 0), bbox_transform = fig.transFigure, loc = "lower right", ncol = 3)
    
        return fig, ax
    
    # GAME PLOTS ================================================================================
    def overlayedGame(self, fig, subject, cond, act):

        positions, gtime, score = self.subjectGame[cond][act][subject]

        # Create 2 subplots, one for player and one for tracker
        ax = fig.subplots(2, 1)

        fig.suptitle('Time based Player and Tracker Position', fontsize = 10)
        fig.supxlabel('Time (s)', fontsize = 10)
        fig.supylabel('Position', fontsize = 10)

        # x-axis will be time stamp
        xaxis = gtime

        ax[0].set_facecolor(self.backplotColor)
        ax[1].set_facecolor(self.backplotColor)

        # Plot Player
        ax[0].plot(xaxis, positions[0], color = self.ftxColor, label = 'x')
        ax[0].plot(xaxis, positions[1], color = self.ftyColor, label = 'y')
        ax[0].plot(xaxis, positions[2], color = self.ftzColor, label = 'z')

        # Plot Tracker
        ax[1].plot(xaxis, positions[3], color = self.ftxColor)
        ax[1].plot(xaxis, positions[4], color = self.ftyColor)
        ax[1].plot(xaxis, positions[5], color = self.ftzColor)

        ax[0].legend(bbox_to_anchor = (1, 0), bbox_transform = fig.transFigure, loc = "lower right", ncol = 3)
    
        return fig, ax
    
    # MIXED PLOTS =============================================================================
    def emgOverGameTime(self, fig, subject, cond, act):
        game, gtime, score = self.subjectGame[cond][act][subject]
        emg, etime = self.subjectEmg[cond][act][subject]

        ax = fig.subplots(self.channels, 1)

        for i in range(self.channels):
            ax[i].plot(etime)
            ax[i].plot(gtime)
        
    def __rmsAndForceHelper(self, fig, subject, cond, act):
        # make subfigures
        subfigs = fig.subfigures(2, 1)

        # plot EMG and force
        self.rmsPlot(subfigs[0], subject, cond, act)
        self.forcePlot(subfigs[1], subject, cond, act)

    def rmsAndForce(self, subject, gender, age, hand, cond, activity):

        fig0 = plt.figure(figsize= (8,11))
        # Place leftside header: subject, gender, dominant hand
        fig0.text(0.01, .95, subject + '\n' + gender + age + '\n' + hand, fontsize=8)

        # Place rightside header: condition, act, score

        fig0.text(.92, .95, str(cond) + '\n' + self.activityOrder[activity-1], fontsize = 8)
        self.__rmsAndForceHelper(fig0, subject, cond-1, activity-1)

        os.chdir('figures')
        os.chdir(f"{subject}_figures")
        plt.savefig(f"{subject}_{cond}_{activity}")
        os.chdir('..')
        os.chdir('..')

        plt.close()
        
    def showPlots(self):
        plt.subplots_adjust()

        plt.show()
