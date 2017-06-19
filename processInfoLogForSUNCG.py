import numpy as np
import csv
from sys import platform

if platform == "linux" or platform == "linux2":
    layoutDirectory='/homes/el216/Workspace/SceneNetData/Layouts'
elif platform == "darwin":
    layoutDirectory='/Users/lingevan/Workspace/SceneNet/SceneNetDataOriginal/Layouts'
layoutFile='/suncg_houses/house2/house.obj'
layoutFilePath = layoutDirectory+layoutFile

mappingCSV = 'ModelCategoryMapping.csv'

if platform == "linux" or platform == "linux2":
    outputDirectory='/scratch/el216/output_scenenet'
elif platform == "darwin":
    outputDirectory='/Users/lingevan/Workspace/SceneNet'

output = '/26May/OutputSceneNet01'

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
    i=0
    j = 0
    for line in r:

        if inFloor or inCeiling or inWall or inObject:
            if line.startswith('usemtl '):
                texture = line.split()[1]
                textures.append(texture)
                insideGroup = True 

        if inObject:
            if line.startswith('g Model#'):
                if not textures == 0: 
                    textureLists.append(textures)
                    i += 1
                textures = []                
                model_id = line.split('#')[1][:-1]
                wnid = getWnidFromModelId(model_id)
                wnidList.append(wnid)

                j += 1

        if not inFloor:
            if line.startswith('g Floor#'):
                inFloor = True
                inCeiling=inWall=inObject = False
                if not textures == 0: 
                    textureLists.append(textures)
                    i += 1
                textures = []
                wnidList.append('03365592') #wnid for Floor
                j += 1
        
        if not inCeiling:
            if line.startswith('g Ceiling#'):
                inCeiling = True
                inFloor=inWall=inObject = False
                if not textures == 0: 
                    textureLists.append(textures)
                    i += 1

                textures = []
                wnidList.append('02990373') #wnid for Ceiling
                j += 1

        if not inWall:
            if line.startswith('g Wall#'):
                inWall = True
                inFloor=inCeiling=inObject = False
                if not textures == 0: 
                    textureLists.append(textures)
                    i += 1

                textures = []
                wnidList.append('04546855') #wnid for Wall
                j += 1

        if not inObject:
            if line.startswith('g Object#'):
                inObject = True
                inFloor=inCeiling=inWall = False
                

    if not textures == 0: 
        textureLists.append(textures)
        i += 1
    print i, j
    return wnidList, textureLists

def matchWnidFromTexture(texture):
    for i, objTextures in enumerate(textureLists):
        if texture in objTextures:
            return wnidList[i]
    return ''

dictList = getCsvDict()
wnidList, textureLists = getWnidMapping()

oldLog = open(outputDirectory + output + '/info.log','rb')
newLog = open(outputDirectory + output + '/infoNew.log','wb')

# first line 
newLog.write(oldLog.readline())

# subsequent lines
for line in oldLog:
    instance, wnid, desc, rest = line.split(';',3)
    if wnid == '':
        wnid = matchWnidFromTexture(desc)
    newLog.write('%s;%s;%s;%s\n' % (instance, wnid, desc, rest[:-1]))








