import numpy as np
import pickle
import sys

houseID = sys.argv[1]
houseObj_filepath = 'suncg/house/' + houseID + '/houseOneFloor.obj'
house_temp_dir = '/homes/el216/Workspace/ScriptsSceneNet/' + houseID + '/'


f = open(house_temp_dir + houseID + '_fromRandomObjects.pckl','rb')
[totalNumObjects, numObjInRooms, objIDs, objWnids, scales, Ts, nullRooms] = pickle.load(f)
f.close()

f2 = open(house_temp_dir + houseID + '_fromOcMap.pckl','rb')
[_, numRooms, cellSide, origin_ocMap, _,
              roomsBBmin, roomsBBmax, roomsSize] = pickle.load(f2)
f2.close()

f3 = open(house_temp_dir + houseID + '_lighting.pckl','rb')
[lights_info, rooms_with_light, lights_in_rooms_byIndex] = pickle.load(f3)
f3.close()

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

for room in rooms_with_light:
    if room not in nullRooms:
        r = room - 1
        ## Header
        w = open(house_temp_dir + houseID + "_" + str(room) + "_scene_description.txt","w")
        w.write('layout_file: ./')
        w.write(houseObj_filepath + '\n')

        ## Objects 
        i = 0
        numBefore = 0
        for numObj in numObjInRooms:
            if (i < r): 
                if numObj: numBefore+= numObj[0]
            else: 
                break
            i += 1

        obj_ids = range(numBefore, numBefore + numObjInRooms[r][0])
        for obj_id in obj_ids:
            w.write('object\n')
            w.write(objWnids[obj_id] + '/' + objIDs[obj_id] + '\n')
            w.write('wnid\n') 
            w.write(objWnids[obj_id] + '\n')
            w.write('scale\n')
            w.write(str(scales[obj_id]))
            w.write('\n')
            w.write('transformation\n')
            np.savetxt(w,Ts[obj_id], fmt='%1.3f')
        w.write('end\n')

        ## Lighting info
        print >> w, 'lighting'
        for index in lights_in_rooms_byIndex[r]:
            print >> w, lights_info[index]

        w.close()
        print 'Generated scene desc txt for room',room,':', \
              houseID+"_"+str(room)+"_scene_description.txt"


# # Room Information for lighting
# print >> w, 'rooms'
# for r in range(numRooms):
#     if not ( np.isnan(roomsBBmin).any() or np.isnan(roomsBBmax).any() ):
#         bbMin_zx = cell2WorldCoord_TopLeft(roomsBBmin[r])
#         bbSize_zx = roomsSize[r] * cellSide
#         print >> w, round(bbMin_zx[0],2), round(bbMin_zx[1],2), \
#                 round(bbSize_zx[0],2), round(bbSize_zx[1],2)

# print houseID,'_scene_description.txt generated with', totalNumObjects, 'objects in and', numRooms,'rooms in scene'

        # for obj in range(totalNumObjects):
        #     w.write('object\n')
        #     w.write(objWnids[obj] + '/' + objIDs[obj] + '\n')
             
        #     w.write('wnid\n') #think it does nothing significant
        #     w.write(objWnids[obj] + '\n')

        #     w.write('scale\n')
        #     w.write(str(scales[obj]))
        #     w.write('\n')

        #     w.write('transformation\n')
        #     np.savetxt(w,Ts[obj], fmt='%1.3f')


        # for line in lights_info:
        #     print >> w, line
