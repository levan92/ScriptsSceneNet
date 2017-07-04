from PIL import Image
import glob
import os
import ntpath
import sys
import shutil
import pickle

houseID = sys.argv[1]
# house_temp_dir = '/homes/el216/Workspace/ScriptsSceneNet/' + houseID + '/'
house_output_temp_dir = "/homes/el216/Workspace/OutputSceneNet/" + houseID + '/'

threshold_rgb = 1.0 # rgb average

if not os.path.exists(house_output_temp_dir):
    sys.exit("Aborting, because output of house given does not exist: "+house_output_temp_dir)

root, rooms_dir_names, _ =  next(os.walk(house_output_temp_dir))

for room_dir in rooms_dir_names:
    room_output_dir = os.path.join(root, room_dir) + '/'

    if not os.path.exists(room_output_dir + "badFrames/"):
        os.makedirs(room_output_dir + "badFrames/")
    if not os.path.exists(room_output_dir + "badFrames/photo/"):
        os.makedirs(room_output_dir + "badFrames/photo/")
    if not os.path.exists(room_output_dir + "badFrames/depth/"):
        os.makedirs(room_output_dir + "badFrames/depth/")
    if not os.path.exists(room_output_dir + "badFrames/instance/"):
        os.makedirs(room_output_dir + "badFrames/instance/")

    print 'In',room_dir,'finding frames that are too dark and moving them away to badFrames'

    for pngfile in glob.glob(room_output_dir + "photo/*.jpg"):
        frameNum = ntpath.basename(pngfile).split('.')[0]
        im = Image.open(pngfile)
        pix = im.load()
        width, height = im.size
        num_pxs = width * height

        rgb = 0.
        for x in range(width):
            for y in range(height):
                rgb += pix[x,y][0]
                rgb += pix[x,y][1]
                rgb += pix[x,y][2]

        avg_rgb = rgb / (num_pxs*3.0)

        if (avg_rgb < threshold_rgb):
            print 'removed frame',frameNum,'avrg rgb',format(round(avg_rgb,2))
            shutil.copy(room_output_dir + "photo/" + frameNum + ".jpg",\
                        room_output_dir + "badFrames/photo/")
            os.unlink(room_output_dir + "photo/" + frameNum + ".jpg")
            shutil.copy(room_output_dir + "depth/" + frameNum + ".png",\
                        room_output_dir + "badFrames/depth/")
            os.unlink(room_output_dir + "depth/" + frameNum + ".png")
            shutil.copy(room_output_dir + "instance/" + frameNum + ".png",\
                        room_output_dir + "badFrames/instance/")
            os.unlink(room_output_dir + "instance/" + frameNum + ".png")

print 'Dark frames moved away.'
            

