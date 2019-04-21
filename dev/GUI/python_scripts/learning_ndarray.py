from numpy import ndarray
from matplotlib import pyplot as plt
from ctypes import c_int16

raw_data = ndarray((3001, 16), int)

with open("binaryFiles/BP76778.C1", "rb") as f:

    i = 0
    j = 0

    # Insert time axis (us)
    while i < 3001:
        raw_data[i][0] = 2 * i
        i += 1

    # Reading data from file
    i = 0
    while i < 15:
        while j < 3001:
            f.seek(2 * (j + 3001 * i))
            raw_data[j][i+1] = int.from_bytes(f.read(2), byteorder='little', signed=True)
            # print(raw_data[i+1][j])
            j += 1
        i += 1
        j = 0
    
print(raw_data[3])
print(raw_data[3].mean())
print(raw_data[3].max())
print(raw_data[3].min())

for item in raw_data:
    print(item[0])
    print(item[1])
    print("\n")

# plt.rcParams["figure.figsize"] = [100.0, 150.0]
# plt.plot(raw_data[0].transpose, raw_data[1:16], subplots=True)
# plt.savefig('detector2.png', bbox_inches='tight')
