import numpy as np
import pickle

f = open('fromRandomObjects.pckl','rb')
totalNumObjects, objIDs, objWnids, scales, Ts = pickle.load(f)
f.close()

houseObj_filepath = 'suncg/house/house2/house.obj'

w = open("scene_description.txt","w")
w.write('layout_file: ./')
w.write(houseObj_filepath + '\n')

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

w.write('end')

print 'scene_description.txt generated with', totalNumObjects, 'objects in scene'