from scipy import misc
import matplotlib.pyplot as plt
import sys
import os

def main(root_folder, suffix):
    vis_folder = os.path.join(root_folder,"Visualisations")

    if not os.path.exists(vis_folder):
        os.mkdir(vis_folder)

    files = next(os.walk(root_folder))[2]

    for file in files: 
        if suffix in file:
            # [basename,ext] = os.path.splitext(file)
            # if ext == ".png":
            print "Generating visualisation for",file
            im_path = os.path.join(root_folder, file)
            new_name = file.replace(suffix, suffix+"_vis") 
            new_path = os.path.join(vis_folder, new_name)
            image = misc.imread(im_path)
            plt.imshow(image,interpolation='nearest')
            plt.colorbar()
            plt.savefig(new_path)
            plt.clf()

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])