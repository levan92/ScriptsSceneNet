#!/bin/sh
# Make sure INIT_Scene.sh is ran first

# Copy generated files to respective directories
cp poses.txt /homes/el216/Workspace/DataSceneNet
cp scene_description.txt /homes/el216/Workspace/DataSceneNet
find /homes/el216/Workspace/OutputSceneNet -type f -delete
cp randomObjectsLocations.txt /homes/el216/Workspace/OutputSceneNet
cp roomsLayout+Objects.png /homes/el216/Workspace/OutputSceneNet

# # Run renderer
cd /homes/el216/Workspace/roboteye/build
./DynamicPose_SceneNet /homes/el216/Workspace/OutputSceneNet /homes/el216/Workspace/DataSceneNet/scene_description.txt
 
# Create Output Folder named after houseID
mkdir /scratch/el216/output_scenenet
# Copy roomsLayout+Objects.png and randomObjectsLocations.txt
