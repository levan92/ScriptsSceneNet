#!/bin/bash

# User Parameters
houses=( 4ddc7eaaff0bb21b58dad10531f55b68\
 4dddeb70f6cf678c261c952451171594\
 4de18a87b301894860d812daa4af131a\
 4de34aa0a3154ef19e4cb2e7445d30e9\
 4de4a408eff4d8a60b667beb4cf6d496\
 4de558b6fbbb24e7a6018ac0d34617a2\
 4de575edb1d56b618ed0f19303fe5ba3\
 4de7b01c53feccf21c7c5d3bcfe32cb1\
 4dea84dc44e5f95a57f38e8d726ec05b\
 4deb6615a6251240f1996b173d902459\
 4dec794666c1f91ff15733163099a010\
 4deea36efca9ecf47ccae52f5795b6f2\
 4df45d0703d98cee71c11ea6602a29b6\
 4df85bf5b284d0f6d8ee9be9aac45802 )

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
mv /homes/el216/Workspace/OutputSceneNet/${houseID} /vol/bitbucket/el216/output_scenenet
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
