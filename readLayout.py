import numpy as np
import matplotlib.path as mplPath


layoutDirectory='/homes/el216/Workspace/SceneNetData/Layouts'
layoutFile='/suncg_houses/house2/house.obj'
layoutFilePath = layoutDirectory+layoutFile

# returns 3D bounds of obj, given how an object is named in the layout file
# for eg, objStr = 'Model#123'
def getObjBounds(layoutFilePath, objStr):
    r = open(layoutFilePath,'r')
    init = True
    inObj = False
    for line in r:
        if line.startswith('g '+ objStr): inObj=True
        
        if inObj:
            if line.startswith('g ') and not line.startswith('g '+objStr): 
                inObj=False
                continue
            elif line.startswith('v '):
                numStr = line[2:].split()
                vec3 = np.array([float(numStr[0]), float(numStr[1]), 
                                 float(numStr[2])])
                if init:
                    x_min = vec3[0]
                    x_max = vec3[0]
                    y_min = vec3[1]
                    y_max = vec3[1]
                    z_min = vec3[2]
                    z_max = vec3[2]
                    init = False
                else:
                    if vec3[0] < x_min: x_min = vec3[0]
                    if vec3[0] > x_max: x_max = vec3[0]
                    if vec3[1] < y_min: y_min = vec3[1]
                    if vec3[1] > y_max: y_max = vec3[1]
                    if vec3[2] < z_min: z_min = vec3[2]
                    if vec3[2] > z_max: z_max = vec3[2]

    return x_min, x_max, y_min, y_max, z_min, z_max

# returns 3D bounds of the entire layout
def getLayoutBounds(layoutFilePath):
    r = open(layoutFilePath,'r')
    init = True
    for line in r:
        if line.startswith('v '):
            numStr = line[2:].split()
            vec3 = np.array([float(numStr[0]), float(numStr[1]), 
                             float(numStr[2])])
            if init:
                x_min = vec3[0]
                x_max = vec3[0]
                y_min = vec3[1]
                y_max = vec3[1]
                z_min = vec3[2]
                z_max = vec3[2]
                init = False
            else:
                if vec3[0] < x_min: x_min = vec3[0]
                if vec3[0] > x_max: x_max = vec3[0]
                if vec3[1] < y_min: y_min = vec3[1]
                if vec3[1] > y_max: y_max = vec3[1]
                if vec3[2] < z_min: z_min = vec3[2]
                if vec3[2] > z_max: z_max = vec3[2]

    return x_min, x_max, y_min, y_max, z_min, z_max


def getFloorHeight():
    _, _, _, y_max, _, _ = getObjBounds(layoutFilePath, 'Floor')
    return y_max

def getRoomsFloor():
    r = open(layoutFilePath,'r')
    rooms = []
    faces = []
    verts = []
    roomCount = 0
    vertIdxCount = 0
    inFloorPre = False
    inFloor = False
    
    for line in r:
        if line.startswith('v '):
            vertIdxCount += 1

        if inFloor: 
            #exit room sequence
            if line.startswith('g '):
                roomCount += 1
                rooms.append(faces)
                faces = []
                verts = []
                inFloor = False
                
            #read verts
            elif line.startswith('v '):
                numStr = line[2:].split()
                vert = [float(numStr[0]), 
                        float(numStr[1]), 
                        float(numStr[2])]
                verts.append(vert)
            #read face, form polygons
            elif line.startswith('f '):
                numStr = line[2:].split()
                faceIndices = [int(numStr[0].split('/')[0]), 
                               int(numStr[1].split('/')[0]), 
                               int(numStr[2].split('/')[0])]
                v1 = verts[faceIndices[0]-startVertIdx-1]
                v2 = verts[faceIndices[1]-startVertIdx-1]
                v3 = verts[faceIndices[2]-startVertIdx-1]
                face = mplPath.Path( np.array([[v1[0],v1[2]],
                                               [v2[0],v2[2]],
                                               [v3[0],v3[2]]]) )
                faces.append(face)

        if inFloorPre:
            if line.startswith('g Floor#'): 
                inFloorPre = False
                inFloor = True
                startVertIdx = vertIdxCount

        if not inFloor:
            if line.startswith('g Floor#'): inFloorPre = True

    return rooms, roomCount