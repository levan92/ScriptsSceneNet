from scipy import misc
import matplotlib.pyplot as plt
import sys
import os
import shutil

root_folder = sys.argv[1]
house = sys.argv[2]

dataset_dir = "/scratch/el216/scenenet_dataset/"
train_dir = os.path.join(dataset_dir, "train")
test_dir = os.path.join(dataset_dir, "test")

vis_folder = os.path.join(root_folder,"Visualisations")
if not os.path.exists(vis_folder):
    os.mkdir(vis_folder)

files = next(os.walk(root_folder))[2]

for file in files: 
    [basename,ext] = os.path.splitext(file)
    if ext == ".png":
        if basename.startswith(house):
            im_path = os.path.join(root_folder, file)
            new_path = os.path.join(vis_folder, basename + "_vis" + ext)
            if os.path.exists(new_path):
                print "Visualisation exists for",file
            else:
                print "Generating visualisation for",file
                image = misc.imread(im_path)
                plt.imshow(image,interpolation='nearest')
                plt.colorbar()
                plt.savefig(new_path)
                plt.clf()
            rgb_name = basename.replace("label","rgb")+".jpg"
            rgb_path = ""
            if rgb_name in next(os.walk(train_dir))[2]:
                rgb_path = os.path.join(train_dir, rgb_name)
            elif rgb_name in next(os.walk(test_dir))[2]:
                rgb_path = os.path.join(test_dir, rgb_name)                
            else: 
                print "RGB frame does not exist for this label."
            if rgb_path:
                shutil.copy(rgb_path, vis_folder)
                print "RGB frame copied into Vis folder too."
    