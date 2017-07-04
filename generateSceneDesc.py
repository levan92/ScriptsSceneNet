import numpy as np
import pickle
import sys
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
from pylab import *

def world2CellCoord(world):
    [z,x] = world
    i = int( np.floor((z - origin_ocMap[0]) / cellSide) )
    j = int( np.floor((x - origin_ocMap[1]) / cellSide) )
    return np.array([i,j])

#visualisation of random object location, current room, light positions and scanning pattern
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

        obj_ids = rooms_obj_ids[r][0]
        for obj_id in obj_ids:
            obj_pos = objs_cell[obj_id]
            plt.scatter(x=obj_pos[1],y=obj_pos[0],c='r',s=10)

        for light_index in lights_in_rooms_byIndex[r]:
            [i,j] = world2CellCoord(lights_pos[light_index])
            plt.plot(j,i,'y^')

        for index,value in ndenumerate(ocMap):
            if value == room: 
                plt.plot(index[1]+2,index[0]+2, 'c*' ) #cyan star
                break

        plt.colorbar(img, cmap=cmap, norm=norm, spacing='proportional', 
                        ticks=bounds, boundaries=bounds, format='%1i')
        ax.set_title('House Map with Lights & Objects')
        savefig(house_temp_dir + houseID+'_'+str(room)+'_RoomMap.png')
        # show()

    return

houseID = sys.argv[1]
houseObj_filepath = 'suncg/house/' + houseID + '/houseOneFloor.obj'
house_temp_dir = '/homes/el216/Workspace/ScriptsSceneNet/' + houseID + '/'

f = open(house_temp_dir + houseID + '_fromRandomObjects.pckl','rb')
[totalNumObjects, numObjInRooms, objIDs, objWnids, scales, Ts, objs_cell] = pickle.load(f)
f.close()

f2 = open(house_temp_dir + houseID + '_fromOcMap.pckl','rb')
[ocMap, numRooms, cellSide, origin_ocMap, _,
 roomsBBmin, roomsBBmax, roomsSize,
 rooms_with_light, lights_in_rooms_byIndex] = pickle.load(f2)
f2.close()

f3 = open(house_temp_dir + houseID + '_lighting.pckl','rb')
[lights_info, lights_pos] = pickle.load(f3)
f3.close()

rooms_obj_ids=[[] for i in range(numRooms)]

for room in rooms_with_light:
    # if room not in nullRooms:
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
    rooms_obj_ids[r].append(obj_ids)
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

#print rooms_obj_ids
#print objs_cell
visualiseMaps()

# #returns world coordinate of the top-left of a given cell
# def cell2WorldCoord_TopLeft(cell):
#     [i,j] = cell
#     z = origin_ocMap[0] + cellSide * i
#     x = origin_ocMap[1] + cellSide * j
#     return np.array([z,x])

# #returns world coordinate of the top-left of a given cell
# def cell2WorldCoord_BotRight(cell):
#     [i,j] = cell
#     z = origin_ocMap[0] + cellSide * (i+1)
#     x = origin_ocMap[1] + cellSide * (j+1)
#     return np.array([z,x])


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
