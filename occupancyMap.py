import matplotlib.path as mplPath
import matplotlib.transforms as mplTrans
import numpy as np
import math
from pylab import *
import readLayout
import pickle
import sys

def getCellBbox(i, j):
    z0 = origin_ocMap[0] + cellSide * i
    z1 = z0 + cellSide
    x0 = origin_ocMap[1] + cellSide * j
    x1 = x0 + cellSide
    return mplTrans.Bbox(np.array([[z0,x0],[z1,x1]]))

def getCellCentre(i, j):
    z = origin_ocMap[0] + cellSide * (i + 0.5)
    x = origin_ocMap[1] + cellSide * (j + 0.5)
    return np.array([z,x])

def initialiseOcMap():
    x_min, x_max, _, _, z_min, z_max = readLayout.getLayoutBounds(layoutFilePath)
    zwidth = z_max - z_min
    iwidth = int(math.ceil(zwidth / cellSide))
    xwidth = x_max - x_min
    jwidth = int(math.ceil(xwidth / cellSide))

    origin_ocMap = [z_min, x_min]
    ocMap = np.zeros((iwidth,jwidth))

    return ocMap, iwidth, jwidth, origin_ocMap

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

    for i, row in enumerate(ocMap):
        for j, roomIdx in enumerate(row):
            if not roomIdx == 0:
                roomIdx = int(roomIdx-1)
                thisCell = np.array([i,j])
                
                if np.isnan(bbs_min[roomIdx][0]).all() or \
                   (thisCell[0] < bbs_min[roomIdx][0]).all():
                    bbs_min[roomIdx][0] = thisCell[0]
                if np.isnan(bbs_min[roomIdx][1]).all() or \
                   (thisCell[1] < bbs_min[roomIdx][1]).all():
                    bbs_min[roomIdx][1] = thisCell[1]

                if np.isnan(bbs_max[roomIdx][0]).all() or \
                   (thisCell[0] > bbs_max[roomIdx][0]).all():
                    bbs_max[roomIdx][0] = thisCell[0]
                if np.isnan(bbs_max[roomIdx][1]).all() or \
                   (thisCell[1] > bbs_max[roomIdx][1]).all():
                    bbs_max[roomIdx][1] = thisCell[1]

    roomsSize = np.zeros((numRooms,2))
    for r in range(numRooms):
        roomsSize[r] = bbs_max[r] - bbs_min[r]

    return bbs_min, bbs_max, roomsSize

def visualiseOcMap():
	fig, ax = plt.subplots()

	# define the colormap
	cmap = plt.cm.jet
	cmaplist = [cmap(i) for i in range(cmap.N)]
	cmaplist[0] = (.5,.5,.5,1.0)
	cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)

	bounds = np.linspace(0,numRooms+1,numRooms+2)
	norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

	img = ax.imshow(ocMap,interpolation='nearest',cmap=cmap, norm=norm)

	plt.colorbar(img, cmap=cmap, norm=norm, spacing='proportional', 
					ticks=bounds, boundaries=bounds, format='%1i')
	ax.set_title('Rooms Layout of House')
	savefig('roomsLayout.png')
	# show()
	return

### 
if __name__ == "__main__":
    houseFilePath = sys.argv[1]
    layoutFilePath = houseFilePath + '/houseOneFloor.obj'

    print 'test'
    # cellSide = .10 # in m
    cellSide = float(sys.argv[2])

    ocMap, iwidth, jwidth, origin_ocMap = initialiseOcMap()

    floorsOfRooms, numRooms = readLayout.getRoomsFloor(layoutFilePath)

    for i in range(iwidth):
    	print 'Occupancy mapping progress: ',round(float(i)/iwidth * 100,2),'%'
    	for j in range(jwidth):
    		cell = getCellBbox(i,j)
    		cellCentre = getCellCentre(i,j)
    		for r in range(numRooms):
    			faces = floorsOfRooms[r]
    			for face in faces:
    				if face.contains_point(cellCentre): ocMap[i,j] = r+1
    				elif face.intersects_bbox(cell, filled=True): ocMap[i,j] = r+1

    roomsBBmin, roomsBBmax, roomsSize = getRoomsInfo(ocMap, numRooms, cellSide)

    floorHeight = readLayout.getFloorHeight(layoutFilePath)

    toSave = [ocMap, numRooms, cellSide, origin_ocMap, floorHeight,
    		  roomsBBmin, roomsBBmax, roomsSize]
    f = open('fromOcMap.pckl','wb')
    pickle.dump(toSave, f)
    f.close()

# visualiseOcMap()			



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

