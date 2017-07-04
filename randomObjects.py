import numpy as np
import pickle
import sys
from sys import platform
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
from pylab import *
import random

# returns 3D bounds of obj
def getObjBounds(objWnid, objID):
    if platform == "linux" or platform == "linux2":
        objectsDirectory='/homes/el216/Workspace/DataSceneNet/Objects'
    elif platform == "darwin":
        objectsDirectory='/Users/lingevan/Workspace/SceneNet/SceneNetDataOriginal/Objects'

    objFile = objectsDirectory + '/' + objWnid + '/' + objID \
                + '/models/model_normalized.obj'
    r = open(objFile,'r')
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
    r.close()
    return x_min, x_max, y_min, y_max, z_min, z_max

def chooseRandObject():
    r = open('smallObjects.txt','r')
    rand = 0
    for line in r:
        if line.startswith('Total'):
            total = int(line.split(':')[1])
            rand = random.randrange(1,total+1) #random int btwn 1 and total
        elif line.startswith(str(rand)):
            num, objWnid, objID, y_height_std, y_sd_std, nickname = line[:-1].split(',')
            break

    return objWnid, objID, float(y_height_std), float(y_sd_std), nickname

def getTmatrix(s, theta_y, d):
    S = np.array([[s[0], 0,    0,    0],
                  [0,    s[1], 0,    0],
                  [0,    0,    s[2], 0],
                  [0,    0,    0,    1]])
    R = np.array([[np.cos(theta_y),0,np.sin(theta_y),0],
                  [0,1,0,0],
                  [-np.sin(theta_y),0,np.cos(theta_y),0],
                  [0,0,0,1]])
    D = np.array([[1, 0, 0, d[0]],
                  [0, 1, 0, d[1]],
                  [0, 0, 1, d[2]],
                  [0, 0, 0,  1 ]])

    T = np.dot(np.dot(D,R),S);
    return T

#returns a positive random number to a normal dist.
def getNormalRand(mean, sd):
    while True: 
        rand = np.random.normal(mean, sd)
        if rand > 0: break
    return rand

#returns world coordinate of the centre of a given cell
def cell2WorldCoord(cell):
    [i,j] = cell
    z = origin_ocMap[0] + cellSide * (i + 0.5)
    x = origin_ocMap[1] + cellSide * (j + 0.5)
    return np.array([z,x])

#returns world coordinate of the top-left of a given cell
def cell2WorldCoord_TopLeft(cell):
    [i,j] = cell
    z = origin_ocMap[0] + cellSide * i
    x = origin_ocMap[1] + cellSide * j
    return np.array([z,x])

#returns cell that contains this world coordinate
def world2CellCoord(world_zx):
    [z,x] = world_zx
    i = int( np.floor((z - origin_ocMap[0]) / cellSide) )
    j = int( np.floor((x - origin_ocMap[1]) / cellSide) )
    return np.array([i,j])

def visualiseMaps():
    for room in rooms_with_light:
        # if room not in nullRooms:
        r = room - 1

        fig, ax = plt.subplots()

        # define the colormap
        cmap = plt.cm.jet
        cmaplist = [cmap(i) for i in range(cmap.N)]
        cmaplist[0] = (.5,.5,.5,1.0)
        cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)

        bounds = np.linspace(0,numRooms+1,numRooms+2)
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

        img = ax.imshow(ocMap,interpolation='nearest',cmap=cmap, norm=norm)

        x = objs_cell[:,1]
        y = objs_cell[:,0]
        plt.scatter(x=x, y=y, c='r', s=10)

        for index,value in ndenumerate(ocMap):
            if value == room: 
                plt.plot(index[1]+2,index[0]+2, 'y*' )
                break

        plt.colorbar(img, cmap=cmap, norm=norm, spacing='proportional', 
                        ticks=bounds, boundaries=bounds, format='%1i')
        ax.set_title('Rooms Layout with objects')
        savefig(house_temp_dir + houseID+'_'+str(room)+'_LayoutAndObjects.png')
        # show()

    return

def writeLogFile():
    f = open(house_temp_dir + houseID+'_randomObjectsLocations.txt','w')
    print >> f, 'Total: ', totalNumObjects, 'objects'
    i = 0
    for room in rooms_with_light:
        # if room not in nullRooms:
        r = room - 1
        print >> f
        print >> f, 'Room',room,':',numObjInRooms[r][0],'objects (', \
                               round(roomsMessiness[r][0]),'% mess )'
        for _ in range(numObjInRooms[r][0]):
            print >> f, '\t', nicknames[i], objs_cell[i], scales[i]
            i += 1;
    return

if __name__ == '__main__':
    houseID = sys.argv[3]
    house_temp_dir = '/homes/el216/Workspace/ScriptsSceneNet/' + houseID + '/'

    f = open (house_temp_dir + houseID+'_fromOcMap.pckl','rb')
    [ocMap, numRooms, cellSide, origin_ocMap, floorHeight,
     roomsBBmin, roomsBBmax, roomsSize, rooms_with_light, _] = pickle.load(f)
    f.close()
    
    # f2 = open (house_temp_dir + houseID+'_lighting.pckl','rb')
    # [_, rooms_with_light, _] = pickle.load(f2)
    # f2.close()

    ## Parameters
    roomsMessMean = float(sys.argv[1])
    roomsMessSD = float(sys.argv[2])
    
    # maxIteration = 10000

    objIDs = []
    objWnids = []
    Ts = []
    scales = []
    objs_cell = np.empty((0,2),int)
    nicknames = []
    numObjInRooms = [[] for i in range(numRooms)]
    roomsMessiness = [[] for i in range(numRooms)]
    totalNumObjects = 0
    nullRooms = []

    print 'Generating random objects for each room...'

    # for r in range(numRooms):
    for room in rooms_with_light:
        r = room - 1

        if np.isnan(roomsBBmin[r]).any() or np.isnan(roomsSize[r]).any():
            numObjects = roomMessiness = 0
            print 'Note: Room', room,'is a null room.'
            nullRooms.append(room)
        else:
            room_origin = cell2WorldCoord_TopLeft(roomsBBmin[r])
            room_zwidth, room_xwidth = roomsSize[r] * cellSide
            area = room_zwidth * room_xwidth
        	# objects per 100m^2
            roomMessiness = getNormalRand(roomsMessMean, roomsMessSD) 
            numObjects = int(round(roomMessiness * (area / 100.))) 
            #numObjects = int(round(getNormalRand(5, 2))) # mean, SD

        # print 'Random objects progress: ', round(float(r)/numRooms * 100,2),'%'

        for obj in range(numObjects):
            [objWnid, objID, y_height_std, 
                        y_sd_std, nickname] = chooseRandObject()
            # TODO: take object size into account in placement
            # x_min, x_max, y_min, y_max, z_min, z_max = getObjBounds(objWnid, objID)
            # objSmallestWidth = min(x_max - x_min, z_max - z_min)
            # objYwidth = y_max - y_min
            y_height = getNormalRand(y_height_std, y_sd_std)
            # scale_factor = y_height / objYwidth
            found = False
            while True:
                rand_zx = np.random.rand(2)
                rand_theta_y = np.random.rand()
                # buf = objSmallestWidth * scale_factor / 2
                d_zx = room_origin + rand_zx * [room_zwidth, room_xwidth]
                theta_y = np.deg2rad(rand_theta_y * 360)
                [i,j] = world2CellCoord(d_zx)
                if ocMap[i,j]==(r+1):
                    found = True
                    break

            # if not found: print 'ERROR: Please check parameters and re-run script. Object location cannot be found within',maxIteration,'iterations.'

            # d_y = floorHeight - 0.6 * y_height
            d_y = floorHeight

            d = np.array([d_zx[1], d_y, d_zx[0]])
            s = np.array([1.,1.,1.])
            T = getTmatrix(s, theta_y, d)

            objIDs.append(objID)
            objWnids.append(objWnid)
            Ts.append(T[0:3])
            scales.append(y_height)
            objs_cell = np.vstack( (objs_cell,world2CellCoord(d_zx)) )
            nicknames.append(nickname)

        roomsMessiness[r].append(roomMessiness)
        numObjInRooms[r].append(numObjects)
        totalNumObjects += numObjects
        print numObjects, 'random objects generated for Room', room

    toSave = [totalNumObjects, numObjInRooms, objIDs, objWnids, scales, Ts, objs_cell]
    f = open(house_temp_dir + houseID+'_fromRandomObjects.pckl','wb')
    pickle.dump(toSave, f)
    f.close()

    print totalNumObjects, 'random objects generated altogether and saved.'

    writeLogFile()

    # visualiseMaps()











