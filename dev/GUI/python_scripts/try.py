def read_data(data):
        return [line.split() for line in data]
        


f=open("/home/tony/Documents/4Tony/P93A.MM", 'r')
print(read_data(f)[0])
f.close()