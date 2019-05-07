import numpy as np
from numpy import ndarray
from matplotlib import pyplot as plt

### Data acquisition (from binary and config files)

# Extracting just the useful data (removing data from broken sensors)
def extract_data(bin_file_name, config_one, config_two):
    bd = bin_data(bin_file_name)
    bd = polarity(bd, config_one)
    num_of_sen = 15
    check = get_sth(config_two, num_of_sen, 1, 1)
    i = 0
    j = 0
    for sen in check:
        if sen == 1:
            bd = np.delete(bd, i-j, 1)
            j+=1
        i+=1

    return bd , num_of_sen-j

# Reading data from a binary file
def bin_data(bin_file_name):

    buf = ndarray((3001, 15), int)

    with open(bin_file_name, "rb") as f:

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
def polarity(bin_data, config):
    num_of_sen = 15
    check = get_sth(config, num_of_sen, 2, 3)
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
def get_sth(config, num_of_sen,num_of_start, num_of_elem):
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
def math_data(config, num_of_sen, bin_data, t):
    den = np.zeros((2,num_of_sen), float)
    den[0] = get_sth(config, num_of_sen,2, 1)
    den[1] = bin_data[int(t/2)]
    return den

# Getting data for main graph
def timed_data(buf, num_of_sens):
    
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
        while i < num_of_sens:
            raw_data[j][1] = raw_data[j][1]+buf[j][i]
            i+=1
        i=0
        j+=1
    return raw_data

# Load binary data to file
def write_to_file(output_file_name, raw_data, num_of_lines):
    with open(output_file_name, "w") as w:
        j=0
        while j<num_of_lines+1:
            w.write(str(raw_data[j])+'\n')
            j+=1


#config_two = "I76778.C1"
#bin_file = "BP76778.C1"

#data, num_of_sens = check_binary_file(bin_file, config_one, config_two)

#print(np.shape(data))
#print(data)
#print("\n")
#print(get_sth(config_two, num_of_sens, 1, 1))
#print("\n")
#print(first_graph_data(data, num_of_sens))

#print(get_sth(config_two, 15, 1, 1))
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
