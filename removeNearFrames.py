from PIL import Image
import glob
import os
import ntpath
import sys
import shutil
import pickle

houseID = sys.argv[1]
house_temp_dir = '/homes/el216/Workspace/ScriptsSceneNet/' + houseID + '/'
house_output_temp_dir = "/homes/el216/Workspace/OutputSceneNet/" + houseID + '/'

threshold_d = 150 # in mm

f = open (house_temp_dir + houseID+'_fromOcMap.pckl','rb')
[_,_,_,_,_,_,_,_,rooms_with_light,_] = pickle.load(f)
f.close()

for room in rooms_with_light:
    # if room not in nullRooms:
    prefix = houseID + "_" + str(room)
    room_output_dir = house_output_temp_dir + prefix + "/"

    if not os.path.exists(room_output_dir + "badFrames/"):
        os.makedirs(room_output_dir + "badFrames/")
    if not os.path.exists(room_output_dir + "badFrames/photo/"):
        os.makedirs(room_output_dir + "badFrames/photo/")
    if not os.path.exists(room_output_dir + "badFrames/depth/"):
        os.makedirs(room_output_dir + "badFrames/depth/")
    if not os.path.exists(room_output_dir + "badFrames/instance/"):
        os.makedirs(room_output_dir + "badFrames/instance/")

    print 'Finding frames that are too near and moving them away to badFrames/'

    for pngfile in glob.glob(room_output_dir + "depth/*.png"):
        frameNum = ntpath.basename(pngfile).split('.')[0]
        im = Image.open(pngfile)
        pix = im.load()
        width, height = im.size
        num_pxs = width * height

        sum_d = 0.0
        for x in range(width):
            for y in range(height):
                d = pix[x,y]
                sum_d += d

        avg_d = sum_d / num_pxs

        if (avg_d < threshold_d):
            print 'removed frame',frameNum,'avrg dist',format(round(avg_d,2)),'mm.'
            shutil.copy(room_output_dir + "photo/" + frameNum + ".jpg",\
                        room_output_dir + "badFrames/photo/")
            shutil.rmtree(room_output_dir + "photo/" + frameNum + ".jpg")
            shutil.copy(room_output_dir + "depth/" + frameNum + ".png",\
                        room_output_dir + "badFrames/depth/")
            shutil.rmtree(room_output_dir + "depth/" + frameNum + ".png")
            shutil.copy(room_output_dir + "instance/" + frameNum + ".png",\
                        room_output_dir + "badFrames/instance/")
            shutil.rmtree(room_output_dir + "instance/" + frameNum + ".png")

print 'Bad frames moved away.'
            

