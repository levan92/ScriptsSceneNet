from PIL import Image
import glob
import os
import ntpath
import sys

photo_path = sys.argv[1]
# house_temp_dir = '/homes/el216/Workspace/ScriptsSceneNet/' + houseID + '/'
# house_output_temp_dir = "/homes/el216/Workspace/OutputSceneNet/" + houseID + '/'

# threshold_rgb = 1.0 # rgb average

if not os.path.exists(photo_path):
    sys.exit("Aborting, because path given does not exist: "+photo_path)

im = Image.open(photo_path)
pix = im.load()
width, height = im.size
num_pxs = width * height

# rgb = 0.
# for x in range(width):
#     for y in range(height):
#         rgb += pix[x,y][0]
#         rgb += pix[x,y][1]
#         rgb += pix[x,y][2]
# avg_rgb = rgb / (num_pxs*3.0)
total_rgb = 0.

for x in range(width):
    for y in range(height):
        rgb = 0.
        rgb = max(rgb,pix[x,y][0])
        rgb = max(rgb,pix[x,y][1])
        rgb = max(rgb,pix[x,y][2])
        total_rgb += rgb;

avg_rgb = total_rgb / num_pxs

print 'Average rgb intensity:',avg_rgb
# if (avg_rgb < threshold_rgb):
#     print 'removed frame',frameNum,'avrg rgb',format(round(avg_rgb,2))
#     shutil.copy(room_output_dir + "photo/" + frameNum + ".jpg",\
#                 room_output_dir + "badFrames/photo/")
#     os.unlink(room_output_dir + "photo/" + frameNum + ".jpg")
#     shutil.copy(room_output_dir + "depth/" + frameNum + ".png",\
#                 room_output_dir + "badFrames/depth/")
#     os.unlink(room_output_dir + "depth/" + frameNum + ".png")
#     shutil.copy(room_output_dir + "instance/" + frameNum + ".png",\
#                 room_output_dir + "badFrames/instance/")
#     os.unlink(room_output_dir + "instance/" + frameNum + ".png")

# print 'Dark frames moved away.'
            

