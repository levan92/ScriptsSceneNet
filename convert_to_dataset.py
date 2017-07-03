import numpy as np
import sys
import os
import shutil

houseID = sys.argv[1]
SET = sys.argv[2]

house_output_temp_dir = "/homes/el216/Workspace/OutputSceneNet/" + houseID + '/'
output_dir = "/scratch/el216/output_scenenet/"
dataset_dir = "/scratch/el216/scenenet_dataset/" + SET + '/' 



if not os.path.exists(output_dir + houseID):
    shutil.copytree(house_output_temp_dir,output_dir)

f = open('dataset_overview.txt','wb')
print >> f, "CNN Dataset Overview"

rooms = next(os.walk(house_output_temp_dir))[1]

for room in rooms:
    room_path = os.path.join(house_output_temp_dir,room)

    folders = next(os.walk(room_path))[1]
    for folder in folders:
        if folder == "photo":
            folder_path = os.path.join(room_path, folder)
            images = next(os.walk(folder_path))[2]
            for image in images:
                if image.endswith(".jpg"):
                    im_path = os.path.join(folder_path,image)
                    basename = os.path.splitext(image)[0]
                    shutil.move(im_path, dataset_dir + houseID + "_" + basename + "_rgb.jpg")
        
        elif folder == "depth":
            folder_path = os.path.join(room_path, folder)
            images = next(os.walk(folder_path))[2]
            for image in images:
                if image.endswith(".png"):
                    im_path = os.path.join(folder_path,image)
                    basename = os.path.splitext(image)[0]
                    shutil.move(im_path, dataset_dir + houseID + "_" + basename + "_depth.png")
        
        elif folder == "label":
            folder_path = os.path.join(room_path, folder)
            images = next(os.walk(folder_path))[2]
            for image in images:
                if image.endswith(".png"):
                    im_path = os.path.join(folder_path,image)
                    basename = os.path.splitext(image)[0]
                    shutil.move(im_path, dataset_dir + houseID + "_" + basename + "_label.png")




# houseID=e9919704131fe1069f73827b53139ff9
# output_directory=/scratch/el216/output_scenenet
# dataset_directory=/scratch/el216/scenenet_dataset
# SET=train
# #SET=test

# echo 'parsing house '$houseID' into dataset format and copying to '$dataset_directory/$SET'.' 

# cd $output_directory/$houseID

# echo 'processing rgb..'
# cd photo
# for i in *.jpg
# do
#     basename=${i%.jpg}
#     cp $i $dataset_directory/$SET/$houseID"_"$basename"_rgb.jpg"    
# done

# echo 'processing labels..'
# cd ../labels
# for i in *.png
# do
#     basename=${i%.png}
#     cp $i $dataset_directory/$SET/$houseID"_"$basename"_label.png"    
# done

# echo 'processing depth..'
# cd ../depth
# for i in *.png
# do
#     basename=${i%.png}
#     cp $i $dataset_directory/$SET/$houseID"_"$basename"_depth.png"    
# done

# echo 'Copied to '$dataset_directory/$SET'.'

# size=$(ls -1 $dataset_directory/$SET | wc -l)
# echo "$SET set current size: $((size/3))"
