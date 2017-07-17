import os, os.path
import linecache
import shutil

def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))

def removeListsFromList(main, lists):
    for l in lists:
        for element in l:
            if element in main:
                main.remove(element)
    return main

output_dir = "/scratch/el216/output_scenenet/"
houses_overview_txt = "/homes/el216/Workspace/ScriptsSceneNet/houses_overview.txt"
dataset_file = "/homes/el216/Workspace/ScriptsSceneNet/dataset_overview.txt"
train_houses = linecache.getline(dataset_file, 3).split()
test_houses = linecache.getline(dataset_file, 5).split()
allocated_houses = train_houses + test_houses

houses = next(os.walk(output_dir))[1]
houses = sorted_ls(output_dir)
# print houses
frames = []
empty_houses = []

f = open(houses_overview_txt,'wb')
print >> f, "SceneNet Dataset -  Houses Overview"
print >> f, "House;Size"

for house in houses:
    house_path = os.path.join(output_dir,house)
    rooms = next(os.walk(house_path))[1]
    size = 0
    for room in rooms:
        room_path = os.path.join(house_path, room)

        folders = next(os.walk(room_path))[1]
        if "badFrames" not in folders:
            print "WARNING:",house,"has not been post-processed!"

        photo_dir_path = os.path.join(room_path,"photo")
        files = next(os.walk(photo_dir_path))[2]
        for file in files:
            if file.endswith(".jpg"): size+=1
    if size == 0: 
        print "Removed",house,"as size is ",size
        shutil.rmtree(os.path.join(output_dir,house))
        empty_houses.append(house)
    else:
        print >> f, house, size
        print house, size

unallocated = removeListsFromList(houses, [allocated_houses, empty_houses])
print >> f, "Unallocated:",unallocated
print "Unallocated:",unallocated

