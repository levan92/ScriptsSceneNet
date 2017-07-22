import os, os.path
import linecache
import shutil
from pathlib import Path

def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))

def removeListsFromList(main, lists):
    for l in lists:
        for element in l:
            if element in main:
                main.remove(element)
    return main

output_dir = "/vol/bitbucket/el216/output_scenenet/"
houses_overview_txt = "/homes/el216/Workspace/ScriptsSceneNet/houses_overview.txt"
dataset_file = "/homes/el216/Workspace/ScriptsSceneNet/dataset_overview.txt"
train_houses = linecache.getline(dataset_file, 3).split()
val_houses = linecache.getline(dataset_file, 5).split()
test_houses = linecache.getline(dataset_file, 7).split()
allocated_houses = train_houses + val_houses + test_houses

houses = sorted_ls(output_dir)
frames = []
empty_houses = []

f = open(houses_overview_txt,'wb')
print >> f, "SceneNet Dataset -  Houses Overview"
print >> f, "House;Size"

for house in houses:
    house_path = os.path.join(output_dir,house)
    size = 0
    for room in os.listdir(house_path):
        room_path = os.path.join(house_path, room)
	if "badFrames" not in os.listdir(room_path):
            print "WARNING:",house,"has not been post-processed!"
        photo_dir_path = os.path.join(room_path,"photo")
	for image in os.listdir(photo_dir_path):
            if image.endswith(".jpg"): 
		size+=1
    if size == 0: 
        print "Removed",house,"as size is ",size
        empty_houses.append(house)
    else:
        print >> f, house, size
        print house, size

unallocated = removeListsFromList(houses, [allocated_houses, empty_houses])
print >> f, "Unallocated:",unallocated
print "Unallocated:",unallocated

