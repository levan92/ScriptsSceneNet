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
SET_base = SET + "_base"

houseID = sys.argv[2]
dataset_txt = "/homes/el216/Workspace/ScriptsSceneNet/dataset_overview.txt"
dataset_dir = "/vol/bitbucket/el216/scenenet_dataset/" + SET_base + '/' 

root, dirs, files = next(os.walk(dataset_dir))

for image in files:
    if image.startswith(houseID):
        im_path = os.path.join(root, image)
        os.remove(im_path)
        # print im_path

print houseID,'removed from',SET_base,'dataset.'

if os.path.exists(dataset_txt):
    with open(dataset_txt,'r') as file:
        data = file.readlines()
else:
    data = []

size = int(len([f for f in os.listdir(dataset_dir)]) / 3.0)
if SET == "train":
    data[1] = "Train base set: size "+str(size)+"\n"
    print 'Train base set current size:',str(size)
    set_houses = data[2].split()
    if houseID not in set_houses:
        set_houses.append(houseID)
    data[2] = ' '.join(set_houses) + "\n"
   
elif SET == "val":
    data[3] = "Val base set: size "+str(size)+"\n"
    print 'Val base set current size:',str(size)
    set_houses = data[4].split()
    if houseID not in set_houses:
        set_houses.append(houseID)
    data[4] = ' '.join(set_houses) + "\n"

elif SET == "test":
    data[5] = "Test base set: size "+str(size)+"\n"
    print 'Test base set current size:',str(size)
    set_houses = data[6].split()
    if houseID not in set_houses:
        set_houses.append(houseID)
    data[6] = ' '.join(set_houses) + "\n"

with open(dataset_txt,'w') as file:
    file.writelines(data)



