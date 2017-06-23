import numpy as np
import csv
import sys
from sys import platform

houseID = sys.argv[1]

if platform == "linux" or platform == "linux2":
    layoutDirectory='/homes/el216/Workspace/DataSceneNet/Layouts'
elif platform == "darwin":
    layoutDirectory='/Users/lingevan/Workspace/SceneNet/SceneNetDataOriginal/Layouts'
layoutFile='/suncg/house/' + houseID + '/houseOneFloor.obj'
layoutFilePath = layoutDirectory + layoutFile

mappingCSV = 'ModelCategoryMapping.csv'

if platform == "linux" or platform == "linux2":
    outputDirectory='/homes/el216/Workspace/OutputSceneNet'
elif platform == "darwin":
    outputDirectory='/Users/lingevan/Workspace/SceneNet'

house_output_dir = outputDirectory + "/" + houseID

def getCsvDict():
    reader = csv.DictReader(open(mappingCSV,'rb'))
    dictList = []
    for line in reader:
        dictList.append(line)
    return dictList

def getWnidFromModelId(model_id):
    for dic in dictList:
        if dic['model_id'] == model_id:
            return dic.get('wnsynsetid')[1:]
    return []

# returns variables that maps from textures of the object to its WNID 
def getWnidMapping():
    r = open(layoutFilePath,'r')
    inFloor = inCeiling = inWall = inObject = False
    wnidList = [] 
    textures = 0
    textureLists = []

    for line in r:

        if inFloor or inCeiling or inWall or inObject:
            if line.startswith('usemtl '):
                texture = line.split()[1]
                textures.append(texture)
                insideGroup = True 

        if inObject:
            if line.startswith('g Model#'):
                if not textures == 0: textureLists.append(textures)
                textures = []                
                model_id = line.split('#')[1][:-1]
                wnid = getWnidFromModelId(model_id)
                wnidList.append(wnid)


        if not inFloor:
            if line.startswith('g Floor#'):
                inFloor = True
                inCeiling=inWall=inObject = False
                if not textures == 0: textureLists.append(textures)
                textures = []
                wnidList.append('03365592') #wnid for Floor
        
        if not inCeiling:
            if line.startswith('g Ceiling#'):
                inCeiling = True
                inFloor=inWall=inObject = False
                if not textures == 0: textureLists.append(textures)
                textures = []
                wnidList.append('02990373') #wnid for Ceiling

        if not inWall:
            if line.startswith('g Wall#'):
                inWall = True
                inFloor=inCeiling=inObject = False
                if not textures == 0: textureLists.append(textures)
                textures = []
                wnidList.append('04546855') #wnid for Wall

        if not inObject:
            if line.startswith('g Object#'):
                inObject = True
                inFloor=inCeiling=inWall = False

    if not textures == 0: textureLists.append(textures)

    return wnidList, textureLists

def matchWnidFromTexture(texture):
    for i, objTextures in enumerate(textureLists):
        if texture in objTextures:
            return wnidList[i]
    return ''

print 'Generating infoNew.log ...'


dictList = getCsvDict()
wnidList, textureLists = getWnidMapping()

oldLog = open(house_output_dir + '/info.log','rb')
newLog = open(house_output_dir + '/infoNew.log','wb')

# first line 
newLog.write(oldLog.readline())

# subsequent lines
for line in oldLog:
    instance, wnid, desc, rest = line.split(';',3)
    if wnid == '':
        wnid = matchWnidFromTexture(desc)
    newLog.write('%s;%s;%s;%s\n' % (instance, wnid, desc, rest[:-1]))

print 'infoNew.log generated.'







