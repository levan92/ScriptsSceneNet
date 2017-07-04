import numpy as np
import sys
import os
import shutil

def getParentName(path):
    return os.path.basename(os.path.abspath(os.path.join(path, os.pardir)))

houseID = sys.argv[1]
SET = sys.argv[2]

house_output_temp_dir = "/homes/el216/Workspace/OutputSceneNet/" + houseID + '/'
output_dir = "/scratch/el216/output_scenenet/"
dataset_dir = "/scratch/el216/scenenet_dataset/" + SET + '/' 

if not os.path.exists(output_dir + houseID):
    shutil.copytree(house_output_temp_dir,output_dir)

for root, dirs, files in os.walk(house_output_temp_dir):
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
            print "RGB images of",parent,'has been copied to',SET,'datset'

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
            print "Depth pngs of",parent,'has been copied to',SET,'datset'

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
            print "Label pngs of",parent,'has been copied to',SET,'datset'

if os.path.exists('dataset_sizes.txt'):
    with open('dataset_sizes.txt','r') as file:
        data = file.readlines()
else:
    data = []

if len(data) < 3:
    data = []
    data.append("CNN Dataset Size Overview\n")
    data.append("Train Set:\n")
    data.append("Test Set:\n")

size = int(len([f for f in os.listdir(dataset_dir)]) / 3.0)
if SET == "train":
    data[1] = "Train Set: "+str(size)+"\n"
    print 'Train set current size:',str(size)
elif SET == "test":#
    data[2] = "Test Set: "+str(size)+"\n"
    print 'Test set current size:',str(size)

with open('dataset_sizes.txt','w') as file:
    file.writelines(data)


