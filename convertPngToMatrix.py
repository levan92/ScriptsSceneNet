from scipy import misc
import glob
import matplotlib.pyplot as plt
import ntpath
import os

# make sure folder ends with a slash /
folder = "/Users/lingevan/Workspace/SceneNet/29May/OutputSceneNet01good/"


if not os.path.exists(folder+"depth/original"):
    os.makedirs(folder+"depth/original")
if not os.path.exists(folder+"depth/proccessedVisualisation"):
    os.makedirs(folder+"depth/proccessedVisualisation")

for image_path in glob.glob(folder+"depth/*.png"):
    imageName=ntpath.basename(image_path)
    print 'processing depth ', imageName
    plt.clf()
    image = misc.imread(image_path)
    
    plt.imshow(image,interpolation='nearest')
    plt.colorbar()    
    plt.savefig(folder+'/depth/proccessedVisualisation/mat_'+imageName)

    os.rename(image_path, folder+'/depth/original/'+imageName)


if not os.path.exists(folder+"instance/original"):
    os.makedirs(folder+"instance/original")
if not os.path.exists(folder+"instance/proccessedVisualisation"):
    os.makedirs(folder+"instance/proccessedVisualisation")

for image_path in glob.glob(folder+"instance/*.png"):
    imageName=ntpath.basename(image_path)
    print 'processing instance', imageName
    plt.clf()
    image = misc.imread(image_path)
    
    plt.imshow(image,interpolation='nearest')
    plt.colorbar()    
    plt.savefig(folder+'/instance/proccessedVisualisation/mat_'+imageName)

    os.rename(image_path, folder+'/instance/original/'+imageName)


if not os.path.exists(folder+"labels/original"):
    os.makedirs(folder+"labels/original")
if not os.path.exists(folder+"labels/proccessedVisualisation"):
    os.makedirs(folder+"labels/proccessedVisualisation")

for image_path in glob.glob(folder+"labels/*.png"):
    imageName=ntpath.basename(image_path)
    print 'processing label', imageName
    plt.clf()
    image = misc.imread(image_path)
    
    plt.imshow(image,interpolation='nearest')
    plt.colorbar()    
    plt.savefig(folder+'/labels/proccessedVisualisation/mat_'+imageName)

    os.rename(image_path, folder+'/labels/original/'+imageName)


