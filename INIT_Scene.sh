#!/bin/sh

houseID=fffeb1ec4c22ee4b96aa8f8acc564721

# Generate .obj and .mtl files from .json
cd /homes/el216/Workspace/DataSceneNet/Layouts/suncg/house/$houseID
/homes/el216/Workspace/SUNCGtoolbox/gaps/bin/x86_64/scn2scn house.json house.obj
pwd ; ls

cd /homes/el216/Workspace/ScriptsSceneNet
python convertToOneFloorObj.py $houseID


# cd '/homes/el216/Workspace/ScriptsSceneNet'

# python occupancyMap.py
# python randomObjects.py
# python generateSceneDesc.py
# python generatePoses.py
