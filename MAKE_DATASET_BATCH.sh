#!/bin/bash

# User Parameters
houses=( c6aa4011efde54ae9522dfacffa29a81\
 c6ab8396a6dcae84981e0311589272ee\
 c6ad956b0f7abc69c452414f6015e9a5\
 c6afba70260fb5876728d968b10a642a\
 c6b8ac173309d4ddebee7e6666680e57\
 c6ba5ff1317906e77b1ff6baf2f31130\
 c6bbe0175b98aae61d352a7858b40b97\
 e765eda5970ac5231b2b374ea106a60e\
 e767f1cbffab230d746b25a1ef9f1a15\
 e76b3dd6314acedd630b49cd2114ae0c\
 e76c73638f1fac7fed56de3b6282aade\
 e76f94ce00b7cc334aaca9778f687355\
 e7715dcce15419abd41ae1ccac464a81\
 e771d95b5406efd99d70bc48fe333d7a\
 e778c9d8c08ab430fa5240f09b10d753\
 e779057fe049efeb04b9227651834c95\
 e77a027d808e4a5bbff199547b14831c\
 e77d1ea48db5f7f2e9c8c736dba72f5c\
 e77d5546b596f1c0847ed7a20efd6f70\
 e7824e894768034bff41d4ddd302bf09 )

for houseID in "${houses[@]}"
do
    
#export CUDA_VISIBLE_DEVICES="4"
echo "Using GPU device "${CUDA_VISIBLE_DEVICES}".." \
    | tee logs/${houseID}_run.log

ocMapCellSide=0.1 # in m, must be small enough 
roomMessMean=40 # in num objs per 100m^2
roomMessSD=10
frameStep=20 # for poses, Frame period = frameStep * 0.1s
# pow_scaling_factor=0.075 # affects brightness of scene
pow_scaling_factor=0.1 # affects brightness of scene

echo 'houseID: '$houseID | tee -a logs/${houseID}_run.log

# Generate .obj and .mtl files from .json
cd /homes/el216/Workspace/DataSceneNet/Layouts/suncg/house/$houseID
/homes/el216/Workspace/SUNCGtoolbox/gaps/bin/x86_64/scn2scn house.json house.obj

cd /homes/el216/Workspace/ScriptsSceneNet
mkdir -p /homes/el216/Workspace/ScriptsSceneNet/$houseID
# Convert .obj file to only one floor
python -u convertToOneFloorObj.py \
  /homes/el216/Workspace/DataSceneNet/Layouts/suncg/house/$houseID \
  | tee -a logs/${houseID}_run.log
# Get lighting information from house json file
# Outputs: $houseID_lighting.pckl
python -u getLighting.py ${houseID} $pow_scaling_factor | tee -a logs/${houseID}_run.log
# Create occupancy map from house obj
# Outputs: fromOcMap.pckl, roomsLayout.png
python -u occupancyMap.py ${houseID} $ocMapCellSide | tee -a logs/${houseID}_run.log
# Generate random objects for house
# Arguments: Room Messiness Mean, SD in num objs per 100m^2, houseID
# Outputs: fromRandomObjects.pckl, 
#          for each room: roomsLayout+Objects.png, randomObjectsLocations.txt
python -u randomObjects.py $roomMessMean $roomMessSD $houseID \
    | tee -a logs/${houseID}_run.log
# Generate SceneDescription txt from random objects and lighting, for each room
# Outputs: houseID_roomNum_scene_description.txt
python -u generateSceneDesc.py $houseID | tee -a logs/${houseID}_run.log
# Generate Poses.txt from room info from occupancymap.py for each room
# Outputs: houseID_roomNum_poses.txt
python -u generatePoses.py $houseID $frameStep | tee -a logs/${houseID}_run.log

# another python script will be iterate through each room with light:
# do directory organisation and run renderer. 
# output directory: house/house_roomNum/output_files.
python -u RunScenenetEachRoom.py $houseID | tee -a logs/${houseID}_run.log

# Filter away bad frames that have too near viewpoints
python -u removeNearFrames.py $houseID | tee -a logs/${houseID}_run.log
# Filter away dark frames
python -u removeBlackFrames.py $houseID | tee -a logs/${houseID}_run.log
# Generate new Log file
python -u processInfoLogForSUNCG.py $houseID | tee -a logs/${houseID}_run.log
# Generate Label pngs from Instance pngs
python -u instance2classFromInfoLog.py $houseID | tee -a logs/${houseID}_run.log

echo 'All post-processing done for House '$houseID | tee -a logs/${houseID}_run.log

# cp -r /homes/el216/Workspace/OutputSceneNet/${houseID} /homes/el216/Workspace/OutputSceneNet/Moved
mv /homes/el216/Workspace/OutputSceneNet/${houseID} /scratch/el216/output_scenenet
echo 'House '${houseID}' moved to scratch'

done


# Copy output to folder named after houseID saved in /scratch drive's output directory
# if [ ! -e /scratch/el216/output_scenenet/${houseID}/ ];
# then
#     mkdir /scratch/el216/output_scenenet/$houseID
#     cp -r ${output_temp_dir}/* /scratch/el216/output_scenenet/$houseID
#     echo 'Output files of house '$houseID' copied to /scratch/el216/output_scenenet/'$houseID | tee -a logs/${houseID}_run.log
#     # rm -r ${output_temp_dir}
#     # echo "Removed temp output directory: "${output_temp_dir} \
#     #     tee -a logs/${houseID}_run.log
        
# else
#     read -p "House "$houseID" output folder exists already. Overwrite contents?" -n 1 -r
#     echo
#     if [[ $REPLY =~ ^[Yy]$ ]]
#     then
#         rm -r /scratch/el216/output_scenenet/$houseID/* 
#         cp -r ${output_temp_dir}/* /scratch/el216/output_scenenet/$houseID
#         echo 'Output files of house '$houseID' overwritten to /scratch/el216/output_scenenet/'$houseID | tee -a logs/${houseID}_run.log
#         rm -r ${output_temp_dir}
#         echo "Removed temp output directory: "${output_temp_dir} \
#             tee -a logs/${houseID}_run.log   
#     else
#         echo 'Output files not moved to /scratch drive' \
#             | tee -a logs/${houseID}_run.log
#             rm -r ${output_temp_dir}
#         echo "Output staying in temp output directory: "${output_temp_dir} \
#         tee -a logs/${houseID}_run.log
#     fi
# fi

# rm -r /homes/el216/Workspace/DataSceneNet/${houseID}_*
# echo "Removed scene desc txt and pose txt from DataSceneNet directory." \
#      | tee -a logs/${houseID}_run.log

# read -p "Remove "$houseID" files from preprocessing? (e.g., fromOcMap.pckl, etc." -n 1 -r
#     echo
#     if [[ $REPLY =~ ^[Yy]$ ]]
#     then
#         rm -r /homes/el216/Workspace/ScriptsSceneNet/${houseID}_*
#         echo "Preprocessing files from py scripts removed." \
#             | tee -a logs/${houseID}_run.log
           
#     else
#         echo 'Preprocessing files from py scripts NOT removed.' \
#             | tee -a logs/${houseID}_run.log
#     fi
