import findObject 
import argparse
from scandir import scandir
import os.path
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('labels_dir',type=str,help='dirs where pred labels stored')
parser.add_argument('cam_info_dir',type=str,help='dir where cam_info_txts are stored')
args = parser.parse_args()

all_objs_loc = []
for label in scandir(args.labels_dir):
    if label.is_file() and label.name.endswith('_label.png'):
        house, room, frame, suffix = label.name.split('_')
        cam_info_txt = os.path.join(args.cam_info_dir,
                                    room+'_'+frame+'_camInfo.txt')
        if os.path.exists(cam_info_txt):
            print 'Finding objects for room',room,',frame',frame,'..'
            objs_loc = findObject.main(label.path, cam_info_txt)
            all_objs_loc.append([objs_loc])
        else:
            print 'camInfo_txt for Room',room,', frame',frame,'does not exists!'

print "Total num of objs in room",len(all_objs_loc)
print np.shape(all_objs_loc)
