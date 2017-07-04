from scipy import misc
import glob
import matplotlib.pyplot as plt
import ntpath
import os

# make sure folder ends with a slash /
outputFolder = "/Users/lingevan/Workspace/SceneNet/29May/OutputSceneNet01good/"

photoFolder = outputFolder + "photo/"

wantList = []
for file in os.listdir(photoFolder):
    if file.endswith('.jpg'):
        newFile = file.replace('.jpg','.png')
        wantList.append(newFile)

depthFolder = outputFolder + 'depth/'
instanceFolder = outputFolder + 'instance/'

for file in os.listdir(depthFolder):
    if file not in wantList:
        os.remove(depthFolder + file)
        os.remove(instanceFolder + file)
        print 'removed ',file




