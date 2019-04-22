import numpy as np
from numpy import ndarray
from matplotlib import pyplot as plt
from ctypes import c_int16

buf = ndarray((3001, 15), int)
raw_data = np.zeros((3001,2), int)

#parsing from config
def read_data(data):
        return [line.split() for line in data]
        
def get_sth(data, num_of_sen, num_of_elem):
        a = np.zeros(num_of_sen)
        s = read_data(data)
        i = 1
        while i < num_of_sen+1:
                a[i-1]=s[i][num_of_elem]
                i+=1
        return a

#======================================================

#parsing from binary file
with open("/home/tony/Documents/4Tony/BP76778.C1", "rb") as f:

    i = 0
    j = 0

    while i < 15:
        while j < 3001:
            f.seek(2 * (j + 3001 * i))
            buf[j][i] = int.from_bytes(f.read(2), byteorder='little', signed=True)
            j += 1
        i += 1
        j = 0

    i=0

#======================================================

    #Insert time axis (us)
    while i < 3001:
        raw_data[i][0] = 2 * i
        i += 1
    
    i=0
    j=0
    
#======================================================

    #Sum all sensors
    while j<3001:
        while i < 15:
            raw_data[j][1] = raw_data[j][1]+buf[j][i]
            i+=1
        i=0
        j+=1

#======================================================

#upload binary data to file
with open("/home/tony/Documents/4Tony/Data_Sum.txt", "w") as w:
    j=0
    while j<3001:
        w.write(str(raw_data[j])+'\n')
        j+=1
        
#======================================================


#print(buf)
print(raw_data)

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
