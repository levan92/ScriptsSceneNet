README
The following directory contains scripts that support the rendering of SUNCG houses using SceneNet-RBGD renderer, for the purpose of generating a dataset of POVs from a robotic vacuum cleaner camera of small objects on the floor of a house. It also contains some scripts with post-processing functions after the render is done.

1) MAKE_DATASET.sh & MAKE_DATASET_BATCH.sh

2) convertToOneFloorObj.py

3) checkLighting.py & checkLightingBatch.py

4) occupancyMap.py
	By using "readLayout.py" and receiving information regarding the faces of the floor of
	each room in the house, an occupancy map of the different rooms in the house is
	generated. 

	Output from this includes the occupancy map and its accompany information, stored in the
	form of a pickle file "fromOcMap.pckl". The occupancy map is also visualised and saved as
	"roomsLayout.png"

	Further improvement hopes to add information of other furnitures/obstacles to the
	occupancy map.

	Output files: fromOcMap.pckl, roomsLayout.png

5) randomObjects.py
	Generates random small objects to be placed in each room of the house. Each room is
	randomly defined a messiness index (0 - 100%), and from that index the number of objects
	in the room. 

	Then, from the set of objects and their respective standard sizes defined in
	"smallObjects.txt", objects are randomly picked and randomly placed in the room. 

	The information on the objects and their location are stored in pickle file
	"fromRandomObjects.pckl". Also, their locations are visualised and plotted over the
	occupancy map, stored as "roomsLayout+Objects.png". A log file
	"randomObjectsLocations.txt" is also written for user to refer to when they look at the
	visualised map.

	Input files: smallObjects.txt, fromOcMap.pckl
	Output files: fromRandomObjects.pckl, roomsLayout+Objects.png, randomObjectsLocations.txt

6) generateSceneDesc.py
	Generates "scene_description.txt" for SceneNet renderer. Reads the random objects
	variables from "randomObjects.py" and writes them in the format required by SceneNet.

	Input file: fromRandomObjects.pckl
	Output file: scene_description.txt

7) generateLookAroundPoses.py:
	Generates "poses.txt" for SceneNet renderer. Takes in room information generated from
	"occupancyMap.py". 

	This set of poses simulates a robotic vaccuum cleaner placed in the approximate centre of
	each room in the house facing forward (negative z direction) and turning 360 degrees. Num
	of frames per room can be specified. 

	Input file: fromOcMap.pckl
	Output file: poses.txt

8) generatePoses.py:
	Generates "poses.txt" for SceneNet renderer. Takes in room information generated from 
	"occupancyMap.py". 

	This set of poses simulates a robotics vaccuum cleaner placed on the top left corner (min
	z and min x) of each room in the house facing right (positive x direction). It then
	attempt to sweep the entire room by undergoing a snake-like scanning pattern: goes
	straight, before hitting the wall it will uturn to its right, goes straight, before
	hitting wall again it will uturn to its left. It terminates its sweep and moves on to the
	next room everytime it is unable make anymore (positive) z-movements. 

	Input file: fromOcMap.pckl
	Output file: poses.txt

9) RunScenenetEachRoom.py

10) getAvrgRGB.py

11) removeNearFrames.py

12) removeBlackFrames.py

13) processInfoLogForSUNCG.py

14) instance2classFromInfoLog.py

15) output_to_dataset.py

16) houses_count.py

17) update_dataset_overview.py

18) data_aug.py & dataAug_targetSize.py

19) findObject.py & findObject_batch.py

20) visualise.py & visualise_batch.py

21) Miscellaneous scripts:
	The following scripts have simple and trivial functions that are written to make some of the repetitive actions more efficient and systematic. Specific functions and usage can be easily read from code:
	- sum_house_sizes.py
	- sample_set.py
	- remove_from_dataset.py
	- remove_aug.py
	- purge_target_files.py



