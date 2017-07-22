import sys
import os
import linecache
from pathlib import Path
import itertools

def main(dataset_dir = None):
    if dataset_dir is None:
        dataset_dir = "/vol/bitbucket/el216/scenenet_dataset/"
    dataset_txt = "/homes/el216/Workspace/ScriptsSceneNet/dataset_overview.txt"

    # train_houses_old = linecache.getline(dataset_txt, 3).split()
    # val_houses_old = linecache.getline(dataset_txt, 5).split()
    # train_houses = []
    # val_houses = []
    # test_houses = []

    sets = ['train_base','val_base','test_base']
    houses_sets = [[] for i in range(len(sets))]
    sizes_sets = []

    for i, set_ in enumerate(sets):
        set_path = os.path.join(dataset_dir,set_)
        n = 0
        for file in Path(set_path):
            if file.endswith(".jpg") or file.endswith(".png"):
                house = file.split('_',1)[0]
                if "aug" in file:
                    aug_str = file.split('_')[3]
                    house = house + "_" + aug_str
                if house not in houses_sets[i]:
                    houses_sets[i].append(house)
                n += 1
        if n%3:
            print "Warning: Something is missing from train"
        sizes_sets.append((n/3.0))
       
    data = []
    data.append("CNN Dataset Overview\n")
    for i, set_  in enumerate(sets):
        set_size = sizes_sets[i]
        set_houses = houses_sets[i]
        data.append(set_,"set: size "+str(set_size)+"\n")
        print set_, 'set current size:',str(set_size)
        data.append(' '.join(set_houses) + "\n")
        print set_,'set houses:',' '.join(set_houses)
        print ''

    with open(dataset_txt,'w') as file:
        file.writelines(data)

    for [i, j] in itertools.combination(range(len(sets)), 2):
        print "Overlapping houses btwn", sets[i], "&", sets[j],":", \
              list(set(houses_sets[i])&set(houses_sets[j]))
    # print "Overlapping houses btwn val & test:", list(set(test_houses)&set(val_houses))
    # print "Overlapping houses btwn train & test:", list(set(train_houses)&set(test_houses))

if __name__ == "__main__":
    if len(sys.argv) == 2: main(sys.argv[1])
    else: main()      
            
       
    # data.append("Val base set: size "+str(val_size)+"\n")
    # print 'Val base set current size:',str(val_size)
    # data.append(' '.join(val_houses) + "\n")
    # print 'Val base set houses:',' '.join(val_houses)
    # print ''

    # data.append("Test base set: size "+str(test_size)+"\n")
    # print 'Test base set current size:',str(test_size)
    # data.append(' '.join(test_houses) + "\n")
    # print 'Test base set houses:',' '.join(test_houses)
    # print ''    # for root, folders, files in os.walk(dataset_dir):
    #     if "train_base" in os.path.basename(root):
    #         train_base_path = os.path.join(dataset_dir,'train_base')
    #         for file in Path():
    #             if file.endswith("_rgb.jpg"):
    #                 house = file.split('_',1)[0]
    #                 if "aug" in file:
    #                     aug_str = file.split('_')[3]
    #                     house = house + "_" + aug_str
    #                 if house not in train_houses:
    #                     train_houses.append(house)
    #                     # print "Appended",house,"to train"
            
    #         total_nfiles = len([f for f in os.listdir(root)])
    #         if total_nfiles%3:
    #             print "Warning: Something is missing from train"
    #         train_size = int(total_nfiles/3)

    #     if "val_base" in os.path.basename(root):
    #         for file in files:
    #             if file.endswith("_rgb.jpg"):
    #                 house = file.split('_',1)[0]
    #                 if "aug" in file:
    #                     aug_str = file.split('_')[3]
    #                     house = house + "_" + aug_str
    #                 if house not in val_houses:
    #                     val_houses.append(house)
    #                     # print "Appended",house,"to val"
    
    #         total_nfiles = len([f for f in os.listdir(root)])
    #         if total_nfiles%3:
    #             print "Warning: Something is missing from val"
    #         val_size = int(total_nfiles/3)

    #     if "test_base" in os.path.basename(root):
    #         for file in files:
    #             if file.endswith("_rgb.jpg"):
    #                 house = file.split('_',1)[0]
    #                 if "aug" in file:
    #                     aug_str = file.split('_')[3]
    #                     house = house + "_" + aug_str
    #                 if house not in test_houses:
    #                     test_houses.append(house)
    #                     # print "Appended",house,"to test"
    
    #         total_nfiles = len([f for f in os.listdir(root)])
    #         if total_nfiles%3:
    #             print "Warning: Something is missing from test"
    #         test_size = int(total_nfiles/3)

    # print train_size
    # print train_houses
    # print "Not recorded in train:", set(train_houses) - set(train_houses_old)
    # print "Not found in folder but listed:", set(train_houses_old) - set(train_houses)
    # print val_size
    # print val_houses
    # print "Not recorded in train:", set(val_houses) - set(val_houses_old)
    # print "Not found in folder but listed:", set(val_houses_old) - set(val_houses)

