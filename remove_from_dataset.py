import numpy as np
import sys
import os
import shutil

def copy_overwrite_tree(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src,dst)

def getParentName(path):
    return os.path.basename(os.path.abspath(os.path.join(path, os.pardir)))

SET = sys.argv[1]
houseID = sys.argv[2]

dataset_dir = "/scratch/el216/scenenet_dataset/" + SET + '/' 

root, dirs, files = next(os.walk(dataset_dir))

for image in files:
    if image.startswith(houseID):
        im_path = os.path.join(root, image)
        os.remove(im_path)
        # print im_path

print houseID,'removed from',SET,'dataset.'

if os.path.exists('dataset_overview.txt'):
    with open('dataset_overview.txt','r') as file:
        data = file.readlines()
else:
    data = []

if len(data) < 5:
    data = []
    data.append("CNN Dataset Overview\n")
    data.append("Train Set:\n")
    data.append("\n")
    data.append("Test Set:\n")
    data.append("\n")

size = int(len([f for f in os.listdir(dataset_dir)]) / 3.0)
if SET == "train":
    data[1] = "Train Set: size "+str(size)+"\n"
    print 'Train set current size:',str(size)
    set_houses = data[2].split()
    if houseID in set_houses:
        set_houses.remove(houseID)
    data[2] = ' '.join(set_houses) + "\n"
   
elif SET == "test":
    data[3] = "Test Set: size "+str(size)+"\n"
    print 'Test set current size:',str(size)
    set_houses = data[4].split()
    if houseID in set_houses:
        set_houses.remove(houseID)
    data[4] = ' '.join(set_houses) + "\n"

with open('dataset_overview.txt','w') as file:
    file.writelines(data)


