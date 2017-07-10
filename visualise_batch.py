from scipy import misc
import matplotlib.pyplot as plt
import sys
import os

root_folder = sys.argv[1]

vis_folder = os.path.join(root_folder,"Visualisations")

if not os.path.exists(vis_folder):
    os.mkdir(vis_folder)

files = next(os.walk(root_folder))[2]

for file in files: 
    [basename,ext] = os.path.splitext(file)
    if ext == ".png":
        print "Generating visualisation for",file
        im_path = os.path.join(root_folder, file)
        new_path = os.path.join(vis_folder, basename + "_vis" + ext)
        image = misc.imread(im_path)
        plt.imshow(image,interpolation='nearest')
        plt.colorbar()
        plt.savefig(new_path)

        plt.clf()