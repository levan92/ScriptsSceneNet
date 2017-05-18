import matplotlib.path as mplPath
import matplotlib.transforms as mplTrans
import numpy as np
import math
from pylab import *
from readLayout import *

def getCellBbox(i, j):
	x0 = origin_ocMap[0] + cellSide * j
	x1 = x0 + cellSide
	z0 = origin_ocMap[1] + cellSide * i
	z1 = z0 + cellSide
	return mplTrans.Bbox(np.array([[x0,z0],[x1,z1]]))

def getCellCentre(i, j):
	x = origin_ocMap[0] + cellSide * (j + 0.5)
	z = origin_ocMap[1] + cellSide * (i + 0.5)
	return np.array([x,z])

def initialiseOcMap():
	x_min, x_max, _, _, z_min, z_max = getLayoutBounds(layoutFilePath)
	
	zwidth = z_max - z_min
	# zwidth = zwidth + (cellSide - zwidth%cellSide)
	iwidth = int(math.ceil(zwidth / cellSide))
	
	xwidth = x_max - x_min
	# xwidth = xwidth + (cellSide - xwidth%cellSide)
	jwidth = int(math.ceil(xwidth / cellSide))

	origin_ocMap = [x_min, z_min]

	ocMap = np.zeros((iwidth,jwidth))

	return ocMap, iwidth, jwidth, origin_ocMap

cellSide = 0.5 # in m

ocMap, iwidth, jwidth, origin_ocMap = initialiseOcMap()

floorsOfRooms, numRooms = getRoomsFloor()

for i in range(iwidth):
	print 'Progress: ',round(float(i)/iwidth * 100,2),'%'
	for j in range(jwidth):
		cell = getCellBbox(i,j)
		cellCentre = getCellCentre(i,j)
		for r in range(numRooms):
			faces = floorsOfRooms[r]
			for face in faces:
				if face.contains_point(cellCentre): ocMap[i,j] = r+1
				elif face.intersects_bbox(cell, filled=True): ocMap[i,j] = r+1
				
			

			# if face.intersects_bbox(cell, filled=True): 
			# 	ocMap[i,j] = 1

# Visualisation of ocMap
np.savetxt('ocMap.txt',ocMap)

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

# setup the plot
fig, ax = plt.subplots(1,1, figsize=(6,6))

# define the colormap
cmap = plt.cm.jet
# extract all colors from the .jet map
cmaplist = [cmap(i) for i in range(cmap.N)]
# force the first color entry to be grey
cmaplist[0] = (.5,.5,.5,1.0)
# create the new map
cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)

# define the bins and normalize
bounds = np.linspace(0,numRooms,numRooms+1)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

# make the scatter
scat = ax.imshow(ocMap,interpolation='nearest',cmap=cmap, norm=norm)

# create a second axes for the colorbar
ax2 = fig.add_axes([0.95, 0.1, 0.03, 0.8])
cb = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, spacing='proportional', ticks=bounds, boundaries=bounds, format='%1i')

ax.set_title('Rooms Layout of House')
ax2.set_ylabel('Room Index')
savefig('roomsLayout.png')
# show()

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

