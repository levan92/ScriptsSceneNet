#!/bin/bash

# User Parameters
# this house doesnt work  houseID=fffeb1ec4c22ee4b96aa8f8acc564721
# houseID=a55f64ca8fdee38a554429d7f7ac8b50
# houseID=fff3ca3254c364df22f15646ad160400
# houseID=ffe9e14822570206cce1fc7259adda71
# houseID=0004dd3cb11e50530676f77b55262d38
# houseID=ffce180f296526fc7488864978f3019a
# houseID=fe3649f602f371d76660b5cb7219c3d0
#houseID=e9919704131fe1069f73827b53139ff9
# doesnt work houseID=dbf9875797a788bd40f7eea3659e7fae
# houseID=03353fe273b81f93a11285c759e8a98b
houseID=b1f1efd51cfa771708d3cf30788d25a0

#export CUDA_VISIBLE_DEVICES="4"
echo "Using GPU device "${CUDA_VISIBLE_DEVICES}".." \
    | tee logs/${houseID}_run.log

ocMapCellSide=0.1 # in m, must be small enough 
roomMessMean=40 # in num objs per 100m^2
roomMessSD=10
frameStep=20 # for poses, Frame period = frameStep * 0.1s

echo 'houseID: '$houseID | tee -a logs/${houseID}_run.log

# Generate .obj and .mtl files from .json
cd /homes/el216/Workspace/DataSceneNet/Layouts/suncg/house/$houseID
/homes/el216/Workspace/SUNCGtoolbox/gaps/bin/x86_64/scn2scn house.json house.obj


cd /homes/el216/Workspace/ScriptsSceneNet
# Convert .obj file to only one floor
python -u convertToOneFloorObj.py \
  /homes/el216/Workspace/DataSceneNet/Layouts/suncg/house/$houseID \
  | tee -a logs/${houseID}_run.log
# Create occupancy map from house obj
# Outputs: fromOcMap.pckl, roomsLayout.png
python -u occupancyMap.py \
  /homes/el216/Workspace/DataSceneNet/Layouts/suncg/house/$houseID \
  $ocMapCellSide | tee -a logs/${houseID}_run.log
# Generate random objects for house
# Arguments: Room Messiness Mean, SD in num objs per 100m^2
# Outputs: fromRandomObjects.pckl, roomsLayout+Objects.png, randomObjectsLocations.txt
python -u randomObjects.py $roomMessMean $roomMessSD $houseID \
    | tee -a logs/${houseID}_run.log
# Generate SceneDescription txt from random objects
# Outputs: scene_description.txt
python -u generateSceneDesc.py $houseID | tee -a logs/${houseID}_run.log
# Generate Poses.txt from room info from occupancymap.py
# Outputs: poses.txt
python -u generatePoses.py $frameStep $houseID | tee -a logs/${houseID}_run.log

# Copy generated files to respective directories
cp ${houseID}_poses.txt /homes/el216/Workspace/DataSceneNet
cp ${houseID}_scene_description.txt /homes/el216/Workspace/DataSceneNet
#find /homes/el216/Workspace/OutputSceneNet -type f -delete
output_temp_dir=/homes/el216/Workspace/OutputSceneNet/${houseID}
mkdir -p ${output_temp_dir}
mkdir -p ${output_temp_dir}/{depth,photo,instance}
cp ${houseID}_randomObjectsLocations.txt $output_temp_dir
cp ${houseID}_LayoutAndObjects.png $output_temp_dir

# Run renderer
cd /homes/el216/Workspace/roboteye/build
./DynamicPose_SceneNet $output_temp_dir \
    /homes/el216/Workspace/DataSceneNet/${houseID}_scene_description.txt /homes/el216/Workspace/DataSceneNet/${houseID}_poses.txt \
    | tee -a /homes/el216/Workspace/ScriptsSceneNet/logs/${houseID}_run.log

cd /homes/el216/Workspace/ScriptsSceneNet
echo 'Frames rendering completed.' | tee -a logs/${houseID}_run.log

# Generate new Log file
python -u processInfoLogForSUNCG.py $houseID | tee -a logs/${houseID}_run.log
# Generate Label pngs from Instance pngs
python -u instance2classFromInfoLog.py $houseID | tee -a logs/${houseID}_run.log

# Copy output to folder named after houseID saved in /scratch drive's output directory
if [ ! -e /scratch/el216/output_scenenet/${houseID}/ ];
then
    mkdir /scratch/el216/output_scenenet/$houseID
    cp -r ${output_temp_dir}/* /scratch/el216/output_scenenet/$houseID
    echo 'Output files of house '$houseID' copied to /scratch/el216/output_scenenet/'$houseID | tee -a logs/${houseID}_run.log
    rm -r ${output_temp_dir}
    echo "Removed temp output directory: "${output_temp_dir} \
        tee -a logs/${houseID}_run.log
        
else
    read -p "House "$houseID" output folder exists already. Overwrite contents?" -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        rm -r /scratch/el216/output_scenenet/$houseID/* 
        cp -r ${output_temp_dir}/* /scratch/el216/output_scenenet/$houseID
        echo 'Output files of house '$houseID' overwritten to /scratch/el216/output_scenenet/'$houseID | tee -a logs/${houseID}_run.log
        rm -r ${output_temp_dir}
        echo "Removed temp output directory: "${output_temp_dir} \
            tee -a logs/${houseID}_run.log   
    else
        echo 'Output files not moved to /scratch drive' \
            | tee -a logs/${houseID}_run.log
            rm -r ${output_temp_dir}
        echo "Output staying in temp output directory: "${output_temp_dir} \
        tee -a logs/${houseID}_run.log
    fi
fi

rm -r /homes/el216/Workspace/DataSceneNet/${houseID}_*
echo "Removed scene desc txt and pose txt from DataSceneNet directory." \
     | tee -a logs/${houseID}_run.log

read -p "Remove "$houseID" files from preprocessing? (e.g., fromOcMap.pckl, etc." -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        rm -r /homes/el216/Workspace/ScriptsSceneNet/${houseID}_*
        echo "Preprocessing files from py scripts removed." \
            | tee -a logs/${houseID}_run.log
           
    else
        echo 'Preprocessing files from py scripts NOT removed.' \
            | tee -a logs/${houseID}_run.log
    fi
