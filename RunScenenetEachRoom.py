import numpy as np
import sys
import shutil
import os
import subprocess
import pickle
import time

houseID = sys.argv[1]

DynamicPoseSceneNet_path = "/homes/el216/Workspace/scenenet/build/DynamicPose_SceneNet"
house_temp_dir = '/homes/el216/Workspace/ScriptsSceneNet/' + houseID + '/'
house_output_temp_dir = "/homes/el216/Workspace/OutputSceneNet/" + houseID + '/'

def mkdir_ifabsent(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    else:
        return False

f = open(house_temp_dir + houseID + '_lighting.pckl','rb')
[_, rooms_with_light, _] = pickle.load(f)
f.close()

f2 = open(house_temp_dir + houseID + '_fromRandomObjects.pckl','rb')
[_, _, _, _, _, _, nullRooms] = pickle.load(f2)
f2.close()

for room in rooms_with_light:
    if room not in nullRooms:

        prefix = houseID + "_" + str(room)
        scene_desc_filepath = house_temp_dir + prefix + "_scene_description.txt"
        poses_filepath = house_temp_dir + prefix + "_poses.txt"
        layout_filepath = house_temp_dir + prefix + "_LayoutAndObjects.png"
        randObjsTxt_filepath = house_temp_dir + houseID + "_randomObjectsLocations.txt"
        lightingTxt_filepath = house_temp_dir + houseID + "_lighting.txt"

        mkdir_ifabsent(house_output_temp_dir)
        room_output_dir = house_output_temp_dir + prefix + "/"
        mkdir_ifabsent(room_output_dir)
        mkdir_ifabsent(room_output_dir + "depth/")
        mkdir_ifabsent(room_output_dir + "photo/")
        mkdir_ifabsent(room_output_dir + "instance/")
        shutil.copy2(layout_filepath,room_output_dir)
        shutil.copy2(randObjsTxt_filepath,room_output_dir)
        shutil.copy2(lightingTxt_filepath,room_output_dir)

        print "Starting scenenet render of Room",room,"of House",houseID,\
              "on GPU",os.environ['CUDA_VISIBLE_DEVICES'],"...\n"
        time.sleep(3)


        scenenet_process = subprocess.Popen([DynamicPoseSceneNet_path, room_output_dir, 
                                              scene_desc_filepath, poses_filepath])
        scenenet_process.wait()
        scenenet_process.terminate()

        # print subprocess.run([DynamicPoseSceneNet_path, room_output_dir, 
                                       # scene_desc_filepath, poses_filepath])

        print "\nCompleted scenenet render of Room",room,"of House",houseID,"."


# #find /homes/el216/Workspace/OutputSceneNet -type f -delete
# output_temp_dir=/homes/el216/Workspace/OutputSceneNet/${houseID}
# mkdir -p ${output_temp_dir}
# mkdir -p ${output_temp_dir}/{depth,photo,instance}
# cp ${houseID}_randomObjectsLocations.txt $output_temp_dir
# cp ${houseID}_LayoutAndObjects.png $output_temp_dir
# cp ${houseID}_lighting.txt $output_temp_dir

# # Run renderer
# cd /homes/el216/Workspace/scenenet/build
# ./DynamicPose_SceneNet $output_temp_dir \
#     /homes/el216/Workspace/DataSceneNet/${houseID}_scene_description.txt \
#     /homes/el216/Workspace/DataSceneNet/${houseID}_poses.txt \
#     | tee -a /homes/el216/Workspace/ScriptsSceneNet/logs/${houseID}_run.log