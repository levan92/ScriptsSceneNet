import argparse
from scandir import scandir
import os.path
import numpy as np
import pickle
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
from pylab import *
import findObject 

def read_objs_loc(txt_path):
    txt = open(txt_path,'r')
    all_objs_loc = []
    for line in txt:
        a,b = line.split()
        all_objs_loc.append(np.array([float(a),float(b)]))
    txt.close()
    return all_objs_loc

def write_objs_loc(objs_loc, txt):
    for obj in objs_loc:
        print >> txt, obj[0], obj[1]

# in: [z,x] coord, out: [i,j] coord
def world2CellCoord(world):
    [z,x] = world
    i = int( np.floor((z - origin_ocMap[0]) / cellSide) )
    j = int( np.floor((x - origin_ocMap[1]) / cellSide) )
    return np.array([i,j])

#visualisation of random objects ground truths and pred
def visualiseMaps(house, room, ocMap, pred_objs, save_dir, roomsBBmin, roomsBBmax):
    r = room - 1
    fig, ax = plt.subplots()
    ax.set_xlim(roomsBBmin[r][1], roomsBBmax[r][1])
    ax.set_ylim(roomsBBmin[r][0], roomsBBmax[r][0])
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
        plt.scatter(x=obj_pos[1],y=obj_pos[0],c='g',s=100,marker='*')
    for obj_zx in pred_objs:
        obj_ij = world2CellCoord(obj_zx)
        plt.scatter(x=obj_ij[1],y=obj_ij[0],c='r',s=10,marker='o')
    # for index,value in ndenumerate(ocMap):
    #     if value == room: 
    #         plt.plot(index[1]+2,index[0]+2, 'c*' ) #cyan star
    #         break
    plt.colorbar(img, cmap=cmap, norm=norm, spacing='proportional', 
                    ticks=bounds, boundaries=bounds, format='%1i')
    ax.set_title('Zoomed Room Map with Objects')
    save_name = house +'_'+ str(room) +'_PredMap.png'
    plt.gca().invert_yaxis()
    savefig(os.path.join(save_dir, save_name))
    # show()
    print save_name,'saved in',save_dir
    return

parser = argparse.ArgumentParser()
parser.add_argument('house',type=str,help='target house')
parser.add_argument('room',type=int,help='target room number')
parser.add_argument('labels_dir',type=str,help='dirs where pred labels stored')
parser.add_argument('cam_info_dir',type=str,help='dir where cam_info_txts are stored')
parser.add_argument('ocmap_pckl',type=str,help='pckl file of ocMap')
parser.add_argument('overall_save_dir',type=str,help='save dir for overall room infos')
parser.add_argument('--found_objs_txt',type=str,help='if txt provided, program loads from it and will not find objects again')
args = parser.parse_args()

room = str(args.room)
house = args.house
f = open(os.path.normpath(args.ocmap_pckl),'rb')
[ocMap, numRooms, cellSide, origin_ocMap, roomsBBmin, roomsBBmax, \
    roomsSize,rooms_obj_ids, objs_cell] = pickle.load(f)
f.close()
objs_loc_txt_path = os.path.join(args.overall_save_dir,'pred_objs_locations.txt')
if args.found_objs_txt:
    print 'Getting predicted object locations from file..'
    all_objs_loc = read_objs_loc(objs_loc_txt_path)
else:
    print 'Finding predicted object locations..'
    objs_loc_txt = open(objs_loc_txt_path,'w')
    all_objs_loc = []
    for label in scandir(args.labels_dir):
        if label.is_file() and label.name.endswith('_label.png'):
            this_house, this_room, frame, suffix = label.name.split('_')
            if this_house == house and this_room == room:
                cam_info_txt = os.path.join(args.cam_info_dir,
                                            room+'_'+frame+'_camInfo.txt')
                if os.path.exists(cam_info_txt):
                    print 'Finding objects for room',room,',frame',frame,'..'
                    objs_loc = findObject.main(label.path, cam_info_txt)
                    if objs_loc:
                        write_objs_loc(objs_loc, objs_loc_txt)
                        all_objs_loc.extend(objs_loc)
                else:
                    print 'camInfo_txt for Room',room,', frame',frame,'does not exists!'
    objs_loc_txt.close()
print 'Total num of objs in room',room,':',len(all_objs_loc)
visualiseMaps(house, int(room), ocMap, all_objs_loc,  args.overall_save_dir, roomsBBmin, roomsBBmax)