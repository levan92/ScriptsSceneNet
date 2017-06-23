import os, os.path

output_dir = "/scratch/el216/output_scenenet/"

houses = next(os.walk(output_dir))[1]
frames = []

f = open('houses_overview.txt','wb')
print >> f, "SceneNet Dataset -  Houses Overview"
print >> f, "House;Size"

for house in houses:
    house_path = os.path.join(output_dir,house)
    path = os.path.join(house_path,"photo")
    size = len([i for i in os.listdir(path)])
    print >> f, house, size
    

