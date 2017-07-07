import os, os.path

output_dir = "/scratch/el216/output_scenenet/"

houses = next(os.walk(output_dir))[1]
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

    # photo_dir_path = os.path.join(house_path, "photo")
    # images = next(os.walk(photo_dir_path))[2]

    # for image in images:
    #     if image.endswith(".jpg"):
    #         size 

    # size = 0
    # for root, dirs, files in os.walk(house_path): 
    #     if os.path.basename(root) == "photo":
    #         size += len([i for i in os.listdir(root)])
    print >> f, house, size
    print house, size
    

