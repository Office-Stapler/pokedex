import json
import os

dir = input('Enter the directory: ')
for i in os.listdir(dir):
    with open(dir + i, 'r') as fread:
        jfile = json.load(fread)
    
    with open(dir + i, 'w') as fwrite:
        json.dump(jfile, fwrite, indent=4)
    print('Prettified ' + i)