import os, os.path
import linecache

def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))

output_dir = "/scratch/el216/output_scenenet/"

dataset_file = "dataset_overview.txt"
train_houses = linecache.getline(dataset_file, 3).split()
test_houses = linecache.getline(dataset_file, 5).split()
allocated_houses = train_houses + test_houses

houses = next(os.walk(output_dir))[1]
houses = sorted_ls(output_dir)
# print houses
frames = []

f = open('houses_overview.txt','wb')
print >> f, "SceneNet Dataset -  Houses Overview"
print >> f, "House;Size"

for house in houses:
    house_path = os.path.join(output_dir,house)
    rooms = next(os.walk(house_path))[1]
    size = 0
    for room in rooms:
        room_path = os.path.join(house_path, room)
        photo_dir_path = os.path.join(room_path,"photo")
        files = next(os.walk(photo_dir_path))[2]
        for file in files:
            if file.endswith(".jpg"): size+=1

    print >> f, house, size
    print house, size

unallocated = list(set(houses) - set(allocated_houses))
print >> f, "Unallocated:",unallocated
print "Unallocated:",unallocated
