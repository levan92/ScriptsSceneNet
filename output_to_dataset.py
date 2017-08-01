import numpy as np
import sys
import os
import shutil

def getParentName(path):
    return os.path.basename(os.path.abspath(os.path.join(path, os.pardir)))

## SYS ARGS:
# Arg 1: set_name, Arg 2,3...: houses

set_name = sys.argv[1]
houses = sys.argv[2:]
# output_dir = "/vol/bitbucket/el216/output_scenenet/"
output_dir = "/scratch/el216/output_scenenet_bk_1stAug/"
#dataset_dir = "/vol/bitbucket/el216/scenenet_dataset/" + set_name + '/' 
dataset_dir = "/scratch/el216/scenenet_dataset/"+set_name+"/"
# dataset_txt = "/homes/el216/Workspace/ScriptsSceneNet/dataset_overview.txt"
# label_dir_name = "labels"
label_dir_name = "labels_2"

if not os.path.exists(dataset_dir):
    os.mkdir(dataset_dir)
    print ("Created new dir,",dataset_dir)

for house in houses:
    house_path = os.path.join(output_dir, house)
    print ("Copying images of",house,"..")
    for room in os.scandir(house_path):
        photo_dir_path = os.path.join(room.path, 'photo')
        for image in os.scandir(photo_dir_path):
            if image.name.endswith(".jpg"):
                frame_num = os.path.splitext(image.name)[0]
                new_name = room.name + '_' + frame_num + '_rgb.jpg'
                new_path = os.path.join(dataset_dir, new_name)
                shutil.copy(image.path, new_path)
        print ("RGB images of",room.name,'has been copied to',
               set_name,'dataset')

        depth_dir_path = os.path.join(room.path, 'depth')
        for image in os.scandir(depth_dir_path):
            if image.name.endswith(".png"):
                frame_num = os.path.splitext(image.name)[0]
                new_name = room.name + '_' + frame_num + '_depth.png'
                new_path = os.path.join(dataset_dir, new_name)
                shutil.copy(image.path, new_path)
        print ("Depth images of",room.name,'has been copied to',
               set_name,'dataset')

        label_dir_path = os.path.join(room.path, label_dir_name)
        for image in os.scandir(label_dir_path):
            if image.name.endswith(".png"):
                frame_num = os.path.splitext(image.name)[0]
                new_name = room.name + '_' + frame_num + '_label.png'
                new_path = os.path.join(dataset_dir, new_name)
                shutil.copy(image.path, new_path)
        print ("Label images of",room.name,'has been copied to',
               set_name,'dataset')

print ("Size in",dataset_dir,":",
       (len([f for f in os.listdir(dataset_dir)])/3.0))

    # if os.path.exists(dataset_txt):
    #     with open(dataset_txt,'r') as file:
    #         data = file.readlines()
    # else:
    #     data = []

    # if len(data) < 5:
    #     data = []
    #     data.append("CNN Dataset Overview\n")
    #     data.append("Train base set:\n")
    #     data.append("\n")
    #     data.append("Val base set:\n")
    #     data.append("\n")
    #     data.append("Test base set:\n")
    #     data.append("\n")

    # size = int(len([f for f in os.listdir(dataset_dir)]) / 3.0)
    # if SET == "train":
    #     data[1] = "Train base set: size "+str(size)+"\n"
    #     print 'Train base set current size:',str(size)
    #     set_houses = data[2].split()
    #     if houseID not in set_houses:
    #         set_houses.append(houseID)
    #     data[2] = ' '.join(set_houses) + "\n"
       
    # elif SET == "val":
    #     data[3] = "Val base set: size "+str(size)+"\n"
    #     print 'Val base set current size:',str(size)
    #     set_houses = data[4].split()
    #     if houseID not in set_houses:
    #         set_houses.append(houseID)
    #     data[4] = ' '.join(set_houses) + "\n"

    # elif SET == "test":
    #     data[5] = "Test base set: size "+str(size)+"\n"
    #     print 'Test base set current size:',str(size)
    #     set_houses = data[6].split()
    #     if houseID not in set_houses:
    #         set_houses.append(houseID)
    #     data[6] = ' '.join(set_houses) + "\n"

    # with open(dataset_txt,'w') as file:
    #     file.writelines(data)


