import numpy as np

# Read file and place data into usuable data structures
# Format should be:
#   - First column is time stamps (optional)
#   - Rest of columns are EMG Data

class fileReader():

    data = np.array(float)
    
    def readFile(self, fileName):
        # Load csv file into 2D array
        self.data = np.loadtxt(fileName, delimiter = ',', dtype=str)


