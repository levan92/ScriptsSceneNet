import numpy as np
import pickle
import sys

houseID = sys.argv[1]
houseObj_filepath = 'suncg/house/' + houseID + '/houseOneFloor.obj'

f = open(houseID+'_fromRandomObjects.pckl','rb')
totalNumObjects, objIDs, objWnids, scales, Ts = pickle.load(f)
f.close()

f2 = open(houseID+'_fromOcMap.pckl','rb')
[_, numRooms, cellSide, origin_ocMap, _,
              roomsBBmin, roomsBBmax, roomsSize] = pickle.load(f2)
f2.close()

#returns world coordinate of the top-left of a given cell
def cell2WorldCoord_TopLeft(cell):
    [i,j] = cell
    z = origin_ocMap[0] + cellSide * i
    x = origin_ocMap[1] + cellSide * j
    return np.array([z,x])

#returns world coordinate of the top-left of a given cell
def cell2WorldCoord_BotRight(cell):
    [i,j] = cell
    z = origin_ocMap[0] + cellSide * (i+1)
    x = origin_ocMap[1] + cellSide * (j+1)
    return np.array([z,x])

# Header
w = open(houseID+"_scene_description.txt","w")
w.write('layout_file: ./')
w.write(houseObj_filepath + '\n')

# Objects
for obj in range(totalNumObjects):
    w.write('object\n')
    w.write(objWnids[obj] + '/' + objIDs[obj] + '\n')
     
    w.write('wnid\n') #think it does nothing significant
    w.write(objWnids[obj] + '\n')

    w.write('scale\n')
    w.write(str(scales[obj]))
    w.write('\n')

    w.write('transformation\n')
    np.savetxt(w,Ts[obj], fmt='%1.3f')

w.write('end\n')

# Room Information for lighting
print >> w, 'rooms'
for r in range(numRooms):
    if not ( np.isnan(roomsBBmin).any() or np.isnan(roomsBBmax).any() ):
        bbMin_zx = cell2WorldCoord_TopLeft(roomsBBmin[r])
        bbSize_zx = roomsSize[r] * cellSide
        print >> w, round(bbMin_zx[0],2), round(bbMin_zx[1],2), \
                round(bbSize_zx[0],2), round(bbSize_zx[1],2)

print houseID,'_scene_description.txt generated with', totalNumObjects, 'objects in and', numRooms,'rooms in scene'