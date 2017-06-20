#!/bin/sh

# User Parameters
houseID=fffeb1ec4c22ee4b96aa8f8acc564721
ocMapCellSide=0.1 # in m, must be small enough 
roomMessMean=40 # in num objs per 100m^2
roomMessSD=10
frameStep=20 # for poses, Frame period = frameStep * 0.1s

echo 'houseID: '$houseID

# Generate .obj and .mtl files from .json
cd /homes/el216/Workspace/DataSceneNet/Layouts/suncg/house/$houseID
/homes/el216/Workspace/SUNCGtoolbox/gaps/bin/x86_64/scn2scn house.json house.obj

cd /homes/el216/Workspace/ScriptsSceneNet

# Convert .obj file to only one floor
python 'convertToOneFloorObj.py' \
	/homes/el216/Workspace/DataSceneNet/Layouts/suncg/house/$houseID

# Create occupancy map from house obj
# Outputs: fromOcMap.pckl, roomsLayout.png
python occupancyMap.py \
	/homes/el216/Workspace/DataSceneNet/Layouts/suncg/house/$houseID \
	$ocMapCellSide

# Generate random objects for house
# Arguments: Room Messiness Mean, SD in num objs per 100m^2
# Outputs: fromRandomObjects.pckl, roomsLayout+Objects.png, randomObjectsLocations.txt
python randomObjects.py $roomMessMean $roomMessSD 

# # Generate SceneDescription txt from random objects
# # Outputs: scene_description.txt
python generateSceneDesc.py $houseID

# # Generate Poses.txt from room info from occupancymap.py
# # Outputs: poses.txt
python generatePoses.py $frameStep

# Copy generated files to respective directories
cp poses.txt /homes/el216/Workspace/DataSceneNet
cp scene_description.txt /homes/el216/Workspace/DataSceneNet
find /homes/el216/Workspace/OutputSceneNet -type f -delete
cp randomObjectsLocations.txt /homes/el216/Workspace/OutputSceneNet
cp roomsLayout+Objects.png /homes/el216/Workspace/OutputSceneNet

# Run renderer
cd /homes/el216/Workspace/roboteye/build
./DynamicPose_SceneNet /homes/el216/Workspace/OutputSceneNet /homes/el216/Workspace/DataSceneNet/scene_description.txt

# Generate new Log file
python processInfoLogForSUNCG.py 
# TODO: ADAPT PYTHON SCRIPT TO TAKE IN ARGUMENT HOUSEID
# Create Output Folder named after houseID
mkdir /scratch/el216/output_scenenet/$houseID
cp -r 
# Copy roomsLayout+Objects.png and randomObjectsLocations.txt


