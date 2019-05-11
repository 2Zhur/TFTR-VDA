import numpy as np
from numpy import ndarray
from matplotlib import pyplot as plt

### Data acquisition (from binary and config files)
class TFTR_dataframe:

    def __init__(self, bin_file_name, config_one, config_two):
        
        self.bin_file_name = bin_file_name
        self.config_one = config_one
        self.config_two = config_two

        self.data, self.num_of_sens = self.extract_data()

    # Extracting just the useful data (removing data from broken sensors)
    def extract_data(self):
        bd = self.bin_data()
        bd = self.polarity(bd, self.config_one)
        num_of_sen = 15
        check = self.check_config(self.config_two, num_of_sen, 1, 1)
        i = 0
        j = 0
        for sen in check:
            if sen == 1:
                bd = np.delete(bd, i-j, 1)
                j+=1
            i+=1

        return bd , num_of_sen-j

    # Reading data from a binary file
    def bin_data(self):

        buf = ndarray((3001, 15), int)

        with open(self.bin_file_name, "rb") as f:

            i = 0
            j = 0

            while i < 15:
                while j < 3001:
                    f.seek(2 * (j + 3001 * i))
                    buf[j][i] = int.from_bytes(f.read(2), byteorder='little', signed=True)
                    j += 1
                i += 1
                j = 0

        return buf

    # Setting the correct polarity
    def polarity(self, bin_data, config):
        num_of_sen = 15
        check = self.check_config(config, num_of_sen, 2, 3)
        i = 0
        j = 0
        for sen in check:
            if sen == -1.0:
                while j<3001:
                    bin_data[j][i]=bin_data[j][i]*(-1)
                    j+=1
                j=0    
            i+=1
        return bin_data

    # Parsing the config file        
    def check_config(self, config, num_of_sen, num_of_start, num_of_elem):
        with open(config, "r") as data:
            buf = [line.split() for line in data]
            a = np.zeros(num_of_sen)
            i = num_of_start-1
            num_of_sen+=i
            j = 1
            while i < num_of_sen:
                a[j-1]=buf[i][num_of_elem]
                i+=1
                j+=1
        return a

    # Getting data for math
    def poloidal_data(self, t):
        den = np.zeros((2, self.num_of_sens), float)
        den[0] = self.check_config(self.config_one, self.num_of_sens, 2, 1)
        den[1] = self.data[int(t/2)]
        return den

    # Getting data for main graph
    def timed_data(self):
        
        raw_data = np.zeros((3001,2), int)
        i=0

        # Insert time axis (us)
        while i < 3001:
            raw_data[i][0] = 2 * i
            i += 1
        
        i=0
        j=0

        # Sum all sensors
        while j<3001:
            while i < self.num_of_sens:
                raw_data[j][1] = raw_data[j][1]+self.data[j][i]
                i+=1
            i=0
            j+=1
        return raw_data

df = TFTR_dataframe("BP76778.C1", "P93A.MM", "I76778.C1")

print(df.poloidal_data(16))

print(df.timed_data())
    #config_two = "I76778.C1"
    #bin_file = "BP76778.C1"

    #data, num_of_sens = check_binary_file(bin_file, config_one, config_two)

    #print(np.shape(data))
    #print(data)
    #print("\n")
    #print(check_config(config_two, num_of_sens, 1, 1))
    #print("\n")
    #print(first_graph_data(data, num_of_sens))

    #print(check_config(config_two, 15, 1, 1))
    #print(data[3].mean())
    #print(data[3].max())
    #print(data[3].min())

    # for item in data:
    #     print(item[0])
    #     print(item[1])
    #     print("\n")

    #plt.rcParams["figure.figsize"] = [100.0, 150.0]
    #plt.plot(data[0].transpose, data[1:16], subplots=True)
    #plt.savefig('detector2.png', bbox_inches='tight')
