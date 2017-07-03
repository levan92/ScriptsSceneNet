import os, os.path

output_dir = "/scratch/el216/output_scenenet/"

houses = next(os.walk(output_dir))[1]
frames = []

f = open('houses_overview.txt','wb')
print >> f, "SceneNet Dataset -  Houses Overview"
print >> f, "House;Size"

for house in houses:
    house_path = os.path.join(output_dir,house)
    size = 0
    for root, dirs, files in os.walk(house_path): 
        if os.path.basename(root) == "photo":
            size += len([i for i in os.listdir(root)])
    print >> f, house, size
    print house, size
    

