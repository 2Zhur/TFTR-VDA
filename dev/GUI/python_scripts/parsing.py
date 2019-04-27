import numpy as np
from numpy import ndarray
from matplotlib import pyplot as plt
from ctypes import c_int16

### Parsing data (with broken sensors)

# Parsing binary file
def bin_data(bin_file):

    buf = ndarray((3001, 15), int)

    with open(bin_file, "rb") as f:

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

# Removing broken sensors
def check_binary_file(bin_data, config):
    num_of_sen = 15
    check = get_sth(config, num_of_sen, 1, 1)
    i = 0
    j = 0
    for sen in check:
        if sen == 1:
            bin_data = np.delete(bin_data, i-j, 1)
            j+=1
        i+=1  
    
    return bin_data , num_of_sen-j   

# Setting the correct polarity
def polarity(bin_data,config):
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
def first_graph_data(buf, num_of_sens):
    
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
def write_to_file(output_file,raw_data,num_of_lines):   
    with open("/home/tony/Documents/4Tony/Data_Sum.txt", "w") as w:
        j=0
        while j<num_of_lines+1:
            w.write(str(raw_data[j])+'\n')
            j+=1


config_one= "/home/tony/Documents/4Tony/P93A.MM"
config_two = "/home/tony/Documents/4Tony/I76778.C1"
bin_file = "/home/tony/Documents/4Tony/BP76778.C1"

data, num_of_sens = check_binary_file(polarity(bin_data(bin_file),config_one), config_two)


print(data)
print("\n")
print(get_sth(config_two, num_of_sens, 1, 1))
print("\n")
#print(first_graph_data(data, num_of_sens))



#print(get_sth(config_two, 15, 1, 1))
#print(raw_data[3].mean())
#print(raw_data[3].max())
#print(raw_data[3].min())

#for item in raw_data:
#    print(item[0])
#    print(item[1])
#    print("\n")

 #plt.rcParams["figure.figsize"] = [100.0, 150.0]
 #plt.plot(raw_data[0].transpose, raw_data[1:16], subplots=True)
 #plt.savefig('detector2.png', bbox_inches='tight')
