from scipy import misc
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
import os
import shutil

def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime, reverse=True))

root_folder = sys.argv[1]
num_images = int(sys.argv[2])

dataset_dir = "/scratch/el216/scenenet_dataset/"
train_dir = os.path.join(dataset_dir, "train")
test_dir = os.path.join(dataset_dir, "test")

vis_folder = os.path.join(root_folder,"Visualisations")
if not os.path.exists(vis_folder):
    os.mkdir(vis_folder)

# files = next(os.walk(root_folder))[2]
files = sorted_ls(root_folder)

i = 0
for file in files: 
    [basename,ext] = os.path.splitext(file)
    if ext == ".png":
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

        i += 1
        if i >= num_images: break        
