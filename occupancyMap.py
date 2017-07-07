import numpy as np
import math
import pickle
import sys
import os.path
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.path as mplPath
import matplotlib.transforms as mplTrans
from pylab import *

def getCellBbox(i, j):
    z0 = origin[0] + cellSide * i
    z1 = z0 + cellSide
    x0 = origin[1] + cellSide * j
    x1 = x0 + cellSide
    return mplTrans.Bbox(np.array([[z0,x0],[z1,x1]]))

def getCellCentre(i, j):
    z = origin[0] + cellSide * (i + 0.5)
    x = origin[1] + cellSide * (j + 0.5)
    return np.array([z,x])

def parseObj(layoutFilePath):
    r = open(layoutFilePath,'rb')
    rooms = []
    faces = []
    verts = []
    houseBB = np.empty((3,2)) # 1st col: min x,y,z min, 2nd col: max x,y,z
    houseBB[:] = np.NAN
    roomsBB_zx = []
    roomBB = np.empty((3,2)) # 1st col: min z,x ; 2nd col: max z,x 
    roomBB[:] = np.NAN
    roomCount = 0
    vertIdxCount = 0
    inFloor = False
    
    for line in r:
        if line.startswith('v '): vertIdxCount += 1
        
        if inFloor: 
            #read verts
            if line.startswith('v '):
                numStr = line[2:].split()
                vert = [float(numStr[0]), 
                        float(numStr[1]), 
                        float(numStr[2])]
                verts.append(vert)

                if np.isnan(roomBB[0,0]) or vert[0] < roomBB[0,0]: 
                    roomBB[0,0] = vert[0] #x_min
                if np.isnan(roomBB[0,1]) or vert[0] > roomBB[0,1]: 
                    roomBB[0,1] = vert[0] #x_max
                if np.isnan(roomBB[1,0]) or vert[1] < roomBB[1,0]: 
                    roomBB[1,0] = vert[1] #y_min
                if np.isnan(roomBB[1,1]) or vert[1] > roomBB[1,1]: 
                    roomBB[1,1] = vert[1] #y_max
                if np.isnan(roomBB[2,0]) or vert[2] < roomBB[2,0]: 
                    roomBB[2,0] = vert[2] #z_min
                if np.isnan(roomBB[2,1]) or vert[2] > roomBB[2,1]: 
                    roomBB[2,1] = vert[2] #z_max
            #read face, form polygons
            elif line.startswith('f '):
                numStr = line[2:].split()
                faceIndices = [int(numStr[0].split('/')[0]), 
                               int(numStr[1].split('/')[0]), 
                               int(numStr[2].split('/')[0])]
                v1 = verts[faceIndices[0]-startVertIdx-1]
                v2 = verts[faceIndices[1]-startVertIdx-1]
                v3 = verts[faceIndices[2]-startVertIdx-1]
                face = mplPath.Path( np.array([[v1[2],v1[0]],
                                               [v2[2],v2[0]],
                                               [v3[2],v3[0]]]) )
                faces.append(face)
            # exit room
            elif line.startswith('g ') and 'Floor#' not in line:
                roomCount += 1
                rooms.append(faces)
                roomBB_zx = np.vstack((roomBB[2],roomBB[0])) 
                roomsBB_zx.append(roomBB_zx)
                if np.isnan(houseBB[0,0]) or roomBB[0,0] < houseBB[0,0]: 
                    houseBB[0,0] = roomBB[0,0] #x_min
                if np.isnan(houseBB[0,1]) or roomBB[0,1] > houseBB[0,1]: 
                    houseBB[0,1] = roomBB[0,1] #x_max
                if np.isnan(houseBB[1,0]) or roomBB[1,0] < houseBB[1,0]: 
                    houseBB[1,0] = roomBB[1,0] #y_min
                if np.isnan(houseBB[1,1]) or roomBB[1,1] > houseBB[1,1]: 
                    houseBB[1,1] = roomBB[1,1] #y_max
                if np.isnan(houseBB[2,0]) or roomBB[2,0] < houseBB[2,0]: 
                    houseBB[2,0] = roomBB[2,0] #z_min
                if np.isnan(houseBB[2,1]) or roomBB[2,1] > houseBB[2,1]: 
                    houseBB[2,1] = roomBB[2,1] #z_max
                faces = []
                verts = []
                roomBB[:]=np.NAN
                inFloor = False

        elif line.startswith('g Floor#'):
            inFloor = True
            startVertIdx = vertIdxCount


    zwidth = houseBB[2,1] - houseBB[2,0] # z_max - z_min
    iwidth = int(math.ceil(zwidth / cellSide))

    xwidth = houseBB[0,1] - houseBB[0,0] # x_max - x_min
    jwidth = int(math.ceil(xwidth / cellSide))

    origin = [houseBB[2,0], houseBB[0,0]]
    ocMap = np.zeros((iwidth,jwidth))

    floorHeight = houseBB[1,1] # y_max

    return [ocMap, iwidth, jwidth, origin, floorHeight, 
            rooms, roomCount, roomsBB_zx]

def world2CellCoord(world):
    [z,x] = world
    i = int( np.floor((z - origin[0]) / cellSide) )
    j = int( np.floor((x - origin[1]) / cellSide) )
    return np.array([i,j])

def cell2WorldCoord(cell):
    [i,j] = cell
    z = origin[0] + cellSide * (i + 0.5)
    x = origin[1] + cellSide * (j + 0.5)
    return np.array([z,x])

def listOflist(size):
    listOflist = list()
    for i in range(0,size):
        listOflist.append( list() )
    return listOflist

def getRoomsInfo(ocMap, numRooms, cellSide):
    # initialise bounding box min and max
    bbs_min = np.empty((numRooms,2))
    bbs_max = np.empty((numRooms,2))
    bbs_min[:] = np.NAN
    bbs_max[:] = np.NAN
    roomsSize = np.empty((numRooms,2))
    roomsSize[:] = np.NAN

    for r in range(numRooms):
        (i_vec,j_vec) = np.where(ocMap == r+1)
        if i_vec.size:
            bbs_min[r,0] = min(i_vec)
            bbs_min[r,1] = min(j_vec)
            bbs_max[r,0] = max(i_vec)
            bbs_max[r,1] = max(j_vec)
            roomsSize[r] = bbs_max[r] - bbs_min[r]

    return bbs_min, bbs_max, roomsSize

def getLightingsInfo():
    rooms_with_light = []
    lights_in_rooms_byIndex = [[] for i in range(numRooms)]
    
    # i = 0
    for i in range(len(lights_pos)):
    # for pos in lights_pos:
        pos = lights_pos[i]
        pos_cell = world2CellCoord(pos)
        if (pos_cell[0] < 0) or (pos_cell[1] < 0) or \
           (pos_cell[0] >= iwidth) or (pos_cell[1] >= jwidth):
            continue
        room = ocMap[pos_cell[0],pos_cell[1]]
        room = int(room)
        if not room == 0:
            if room not in rooms_with_light:
                rooms_with_light.append(room)
            lights_in_rooms_byIndex[room - 1].append(i)
	
	rooms_with_light = list(set(rooms_with_light))
    return rooms_with_light, lights_in_rooms_byIndex

def visualiseOcMap():
	fig, ax = plt.subplots()

	# define the colormap
	cmap = plt.cm.jet
	cmaplist = [cmap(i) for i in range(cmap.N)]
	cmaplist[0] = (.5,.5,.5,1.0)
	cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)

	ticks = np.linspace(0,numRooms+1,numRooms+2)
	norm = mpl.colors.BoundaryNorm(ticks, cmap.N)

	img = ax.imshow(ocMap,interpolation='nearest',cmap=cmap, norm=norm)

	plt.colorbar(img, cmap=cmap, norm=norm, spacing='proportional', 
					ticks=ticks, boundaries=ticks, format='%1i')
	ax.set_title('Rooms Layout of House')
	savefig(house_temp_dir + houseID + '_roomsLayout.png')
	# show()
	return

### 
if __name__ == "__main__":
    print 'Acquiring occupancy map...'

    houseID = sys.argv[1]
    cellSide = float(sys.argv[2])
    # cellSide = .10 # in m
    layoutFilePath='/homes/el216/Workspace/DataSceneNet/Layouts/suncg/house/'+\
                    houseID + '/houseOneFloor.obj'
    house_temp_dir = '/homes/el216/Workspace/ScriptsSceneNet/' + houseID + '/'

    f = open(house_temp_dir + houseID + '_lighting.pckl','rb')
    [lights_info, lights_pos] = pickle.load(f)
    f.close()
    
    [ocMap, iwidth, jwidth, origin, floorHeight, 
    floorsOfRooms, numRooms, roomsBB_zx] = parseObj(layoutFilePath)

    roomsBB_min_cell = np.empty((0,2), int)    
    roomsBB_max_cell = np.empty((0,2), int)
    roomsBB_size_cell = np.empty((0,2), int)

    for r in range(numRooms):
        print 'Updating ocMap with Room',r+1,'out of',numRooms,'rooms'
        roomBB_zx = roomsBB_zx[r]
        topleft_cell = world2CellCoord(roomBB_zx[:,0])
        botright_cell = world2CellCoord(roomBB_zx[:,1])
        num_rows = botright_cell[0] - topleft_cell[0]
        num_cols = botright_cell[1] - topleft_cell[1]
        faces = floorsOfRooms[r]

        for i in range(num_rows):
            for j in range(num_cols):
                cell = topleft_cell + np.array([i,j])
                if ocMap[cell[0],cell[1]] == 0:
                    cell_bbox = getCellBbox(cell[0],cell[1])
                    cellCentre_zx = cell2WorldCoord(cell)
                    for f in faces: 
                        if f.contains_point(cellCentre_zx) or \
                           f.intersects_bbox(cell_bbox, filled=True):
                            ocMap[cell[0],cell[1]] = r+1

    roomsBBmin, roomsBBmax, roomsSize = getRoomsInfo(ocMap, numRooms, cellSide)

    rooms_with_light, lights_in_rooms_byIndex = getLightingsInfo()
    #print rooms_with_light
    #print lights_in_rooms_byIndex

    toSave = [ocMap, numRooms, cellSide, origin, floorHeight,
    		  roomsBBmin, roomsBBmax, roomsSize,
		      rooms_with_light, lights_in_rooms_byIndex]
    f = open(house_temp_dir + houseID + '_fromOcMap.pckl','wb')
    pickle.dump(toSave, f)
    f.close()

    print 'Occupancy map, rooms & lighting info saved.'

    # visualiseOcMap()			


# def initialiseOcMap():
#     x_min, x_max, _, _, z_min, z_max = readLayout.getLayoutBounds(layoutFilePath)
#     zwidth = z_max - z_min
#     iwidth = int(math.ceil(zwidth / cellSide))
#     xwidth = x_max - x_min
#     jwidth = int(math.ceil(xwidth / cellSide))

#     origin_ocMap = [z_min, x_min]
#     ocMap = np.zeros((iwidth,jwidth))

#     return ocMap, iwidth, jwidth, origin_ocMap

# def getRoomsInfo_old(ocMap, numRooms, cellSide):
#     # initialise bounding box min and max
#     bbs_min = np.empty((numRooms,2))
#     bbs_max = np.empty((numRooms,2))
#     bbs_min[:] = np.NAN
#     bbs_max[:] = np.NAN

#     for i, row in enumerate(ocMap):
#         for j, roomIdx in enumerate(row):
#             if not roomIdx == 0:
#                 roomIdx = int(roomIdx-1)
#                 thisCell = np.array([i,j])
                
#                 if np.isnan(bbs_min[roomIdx][0]).all() or \
#                    (thisCell[0] < bbs_min[roomIdx][0]).all():
#                     bbs_min[roomIdx][0] = thisCell[0]
#                 if np.isnan(bbs_min[roomIdx][1]).all() or \
#                    (thisCell[1] < bbs_min[roomIdx][1]).all():
#                     bbs_min[roomIdx][1] = thisCell[1]

#                 if np.isnan(bbs_max[roomIdx][0]).all() or \
#                    (thisCell[0] > bbs_max[roomIdx][0]).all():
#                     bbs_max[roomIdx][0] = thisCell[0]
#                 if np.isnan(bbs_max[roomIdx][1]).all() or \
#                    (thisCell[1] > bbs_max[roomIdx][1]).all():
#                     bbs_max[roomIdx][1] = thisCell[1]

#     roomsSize = np.zeros((numRooms,2))
#     for r in range(numRooms):
#         roomsSize[r] = bbs_max[r] - bbs_min[r]

#     return bbs_min, bbs_max, roomsSize


# if face.intersects_bbox(cell, filled=True): 
# 	ocMap[i,j] = 1

# Visualisation of ocMap
# fig, ax = plt.subplots(1,1, figsize=(6,6))

# # define the colormap
# cmap = plt.cm.jet
# # extract all colors from the .jet map
# cmaplist = [cmap(i) for i in range(cmap.N)]
# # force the first color entry to be grey
# cmaplist[0] = (.5,.5,.5,1.0)
# # create the new map
# cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
# im = imshow(ocMap, cmap=cmap, interpolation='nearest')


# figure(1)
# imshow(ocMap, interpolation='nearest')
# grid(True)

# colorbar()
# show()

# def visualiseOcMap():
# 	# setup the plot
# 	# fig, ax = plt.subplots(1,1, figsize=(6,6))
# 	fig, ax = plt.subplots()

# 	# define the colormap
# 	cmap = plt.cm.jet
# 	# extract all colors from the .jet map
# 	cmaplist = [cmap(i) for i in range(cmap.N)]
# 	# force the first color entry to be grey
# 	cmaplist[0] = (.5,.5,.5,1.0)
# 	# create the new map
# 	cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)

# 	# define the bins and normalize
# 	bounds = np.linspace(0,numRooms,numRooms+1)
# 	norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

# 	# make the scatter
# 	img = ax.imshow(ocMap,interpolation='nearest',cmap=cmap, norm=norm)

# 	# create a second axes for the colorbar
# 	# ax2 = fig.add_axes([0.95, 0.1, 0.03, 0.8])
# 	plt.colorbar(img, cmap=cmap, norm=norm, spacing='proportional', 
# 					ticks=bounds, boundaries=bounds, format='%1i')

# 	ax.set_title('Rooms Layout of House')
# 	savefig('roomsLayout.png')
# 	show()
# 	return

# vertices=[]
# vertices.append( [42.6, 0.05, 37.5] )
# vertices.append( [37.5, 0.05, 37.5] )
# vertices.append( [37.5, 0.05, 43.7] )
# vertices.append( [42.6, 0.05, 43.7] )

# facesIndices = []
# facesIndices.append([1, 2, 3])
# facesIndices.append([3, 4, 1])

# faces = []

# for i in range(len(facesIndices)):
# 	indices = facesIndices[i]
# 	v1 = vertices[indices[0]-1]
# 	v2 = vertices[indices[1]-1]
# 	v3 = vertices[indices[2]-1]
# 	facePolygon = mplPath.Path( np.array([[v1[0],v1[2]],
# 								   		  [v2[0],v2[2]],
# 								   		  [v3[0],v3[2]]]) )
# 	faces.append(facePolygon)

# print facePoly.contains_point([42.5, 37.6])
# print facePoly.intersects_bbox(cell, filled=True)


# def getRoomsInfo(ocMap, numRooms, cellSide):
#     roomsTopLeftCoord = np.empty((numRooms,2))
#     roomsTopLeftCoord[:] = np.NAN
#     roomsCoords = listOflist(numRooms)
    
#     for i, row in enumerate(ocMap):
#         for j, roomIdx in enumerate(row):
#             if not roomIdx == 0.:
#                 roomIdx = int(roomIdx-1)

#                 if np.isnan(roomsTopLeftCoord[roomIdx][0]):
#                     roomsTopLeftCoord[roomIdx] = [i,j]
                
#                 roomsCoords[roomIdx].append([i,j])

#     roomsCoords = np.array(roomsCoords)
#     roomsCentreCoord = np.zeros((numRooms,2))
#     roomsSize = np.zeros((numRooms,2))
    
#     for r in range(numRooms):
#         roomCoords = roomsCoords[r]
#         roomCoords = np.array(roomCoords)
#         iList = list(set(roomCoords[:,0]))
#         roomHeight = len(iList) 
#         mid_i = iList[(roomHeight-1)/2] #integer division
#         midRow = []
#         for coord in roomCoords:
#             if coord[0] == mid_i:
#                 midRow.append(coord)
#         roomWidth = len(midRow)
#         roomsCentreCoord[r] = midRow[(roomWidth-1)/2] #integer division
#         roomsSize[r] = [roomHeight, roomWidth]

#     return roomsTopLeftCoord, roomsCentreCoord, roomsSize

