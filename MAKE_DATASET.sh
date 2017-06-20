#!/bin/bash

# User Parameters
# houseID=fffeb1ec4c22ee4b96aa8f8acc564721
houseID=a55f64ca8fdee38a554429d7f7ac8b50
ocMapCellSide=0.1 # in m, must be small enough 
roomMessMean=40 # in num objs per 100m^2
roomMessSD=10
frameStep=20 # for poses, Frame period = frameStep * 0.1s

echo 'houseID: '$houseID | tee makedataset_logfile.log

# Generate .obj and .mtl files from .json
cd /homes/el216/Workspace/DataSceneNet/Layouts/suncg/house/$houseID
/homes/el216/Workspace/SUNCGtoolbox/gaps/bin/x86_64/scn2scn house.json house.obj


cd /homes/el216/Workspace/ScriptsSceneNet
# Convert .obj file to only one floor
python -u convertToOneFloorObj.py \
	/homes/el216/Workspace/DataSceneNet/Layouts/suncg/house/$houseID | tee -a makedataset_logfile.log
# Create occupancy map from house obj
# Outputs: fromOcMap.pckl, roomsLayout.png
python -u occupancyMap.py \
	/homes/el216/Workspace/DataSceneNet/Layouts/suncg/house/$houseID \
	$ocMapCellSide | tee -a makedataset_logfile.log
# Generate random objects for house
# Arguments: Room Messiness Mean, SD in num objs per 100m^2
# Outputs: fromRandomObjects.pckl, roomsLayout+Objects.png, randomObjectsLocations.txt
python -u randomObjects.py $roomMessMean $roomMessSD | tee -a makedataset_logfile.log
# Generate SceneDescription txt from random objects
# Outputs: scene_description.txt
python -u generateSceneDesc.py $houseID | tee -a makedataset_logfile.log
# Generate Poses.txt from room info from occupancymap.py
# Outputs: poses.txt
python -u generatePoses.py $frameStep | tee -a makedataset_logfile.log


# Copy generated files to respective directories
cp poses.txt /homes/el216/Workspace/DataSceneNet
cp scene_description.txt /homes/el216/Workspace/DataSceneNet
find /homes/el216/Workspace/OutputSceneNet -type f -delete
cp randomObjectsLocations.txt /homes/el216/Workspace/OutputSceneNet
cp roomsLayout+Objects.png /homes/el216/Workspace/OutputSceneNet


# Run renderer
cd /homes/el216/Workspace/roboteye/build
./DynamicPose_SceneNet /homes/el216/Workspace/OutputSceneNet \
/homes/el216/Workspace/DataSceneNet/scene_description.txt | tee -a makedataset_logfile.log
echo 'Frames rendering completed.'

cd /homes/el216/Workspace/ScriptsSceneNet
# Generate new Log file
python -u processInfoLogForSUNCG.py $houseID | tee -a makedataset_logfile.log
# Generate Label pngs from Instance pngs
python -u instance2classFromInfoLog.py | tee -a makedataset_logfile.log


# Copy output to folder named after houseID saved in /scratch drive's output directory
if [ ! -e /scratch/el216/output_scenenet/$houseID/ ];
then
    mkdir /scratch/el216/output_scenenet/$houseID
    cp -r /homes/el216/Workspace/OutputSceneNet/* /scratch/el216/output_scenenet/$houseID
    echo 'Output files of house '$houseID' copied to /scratch/el216/output_scenenet/'$houseID \
        | tee -a makedataset_logfile.log
        
else
    read -p "House "$houseID" output folder exists already. Overwrite contents?" -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        rm -r /scratch/el216/output_scenenet/$houseID/* 
        cp -r /homes/el216/Workspace/OutputSceneNet/* /scratch/el216/output_scenenet/$houseID
        echo 'Output files of house '$houseID' overwritten to /scratch/el216/output_scenenet/'$houseID \
            | tee -a makedataset_logfile.log
           
    else
        echo 'Output files not moved to /scratch drive' | tee -a makedataset_logfile.log
    fi
fi






