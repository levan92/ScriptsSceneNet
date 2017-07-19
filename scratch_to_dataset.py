import numpy as np
import sys
import os
import shutil

def getParentName(path):
    return os.path.basename(os.path.abspath(os.path.join(path, os.pardir)))

SET = sys.argv[1]
SET_base = SET + "_base"
output_dir = "/scratch/el216/output_scenenet/"
dataset_dir = "/scratch/el216/scenenet_dataset/" + SET_base + '/' 
dataset_txt = "/homes/el216/Workspace/ScriptsSceneNet/dataset_overview.txt"

houses = []
for arg in sys.argv[2:]:
    houses.append(arg)

for houseID in houses:
    house_output_dir = os.path.join(output_dir, houseID)

    for root, dirs, files in os.walk(house_output_dir):
        if os.path.basename(root) == "photo":
            parent = getParentName(root)
            if parent != "badFrames":
                for image in files:
                    if image.endswith(".jpg"):
                        im_path = os.path.join(root, image)
                        basename = os.path.splitext(image)[0]
                        shutil.copy(im_path, dataset_dir + parent + "_" + basename + "_rgb.jpg")
                        # print 'moved im_path:', im_path
                        # print 'to dst:', dataset_dir + parent + "_" + basename + "_rgb.jpg"
                print "RGB images of",parent,'has been copied to',SET_base,'dataset'

        if os.path.basename(root) == "depth":
            parent = getParentName(root)
            if parent != "badFrames":
                for image in files:
                    if image.endswith(".png"):
                        im_path = os.path.join(root, image)
                        basename = os.path.splitext(image)[0]
                        shutil.copy(im_path, dataset_dir + parent + "_" + basename + "_depth.png")
                        # print 'moved im_path:', im_path
                        # print 'to dst:', dataset_dir + parent + "_" + basename + "_depth.png"
                print "Depth pngs of",parent,'has been copied to',SET_base,'dataset'

        if os.path.basename(root) == "labels":
            parent = getParentName(root)
            if parent != "badFrames":
                for image in files:
                    if image.endswith(".png"):
                        im_path = os.path.join(root, image)
                        basename = os.path.splitext(image)[0]
                        shutil.copy(im_path, dataset_dir + parent + "_" + basename + "_label.png")
                        # print 'moved im_path:', im_path
                        # print 'to dst:', dataset_dir + parent + "_" + basename + "_label.png"
                print "Label pngs of",parent,'has been copied to',SET_base,'dataset'

    if os.path.exists(dataset_txt):
        with open(dataset_txt,'r') as file:
            data = file.readlines()
    else:
        data = []

    if len(data) < 5:
        data = []
        data.append("CNN Dataset Overview\n")
        data.append("Train base set:\n")
        data.append("\n")
        data.append("Val base set:\n")
        data.append("\n")
        data.append("Test base set:\n")
        data.append("\n")

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


