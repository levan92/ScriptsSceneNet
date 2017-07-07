import numpy as np
import sys
import os
import shutil
import instance2classFromInfoLog_scratch_outputs

output_dir = "/scratch/el216/output_scenenet/"

def removeIfExists(file):
    if os.path.exists(file): 
        os.unlink(file)
        # print "removed",file
    return

# for each house
houses = next(os.walk(output_dir))[1]
for house in houses:

# for each room
    house_path = os.path.join(output_dir, house)
    rooms = next(os.walk(house_path))[1]
    for room in rooms:
        print "In house",house,"room",room

        room_path = os.path.join(house_path, room)
        instance_path = os.path.join(room_path, "instance")
        depth_path = os.path.join(room_path, "depth")
        rgb_path = os.path.join(room_path, "photo")
        labels_path = os.path.join(room_path, "labels")

        badFrames_path = os.path.join(room_path,'badFrames')
        badFrames_depth_path = os.path.join(badFrames_path,'depth')
        badFrames_rgb_path = os.path.join(badFrames_path,'photo')
        badFrames_instance_path = os.path.join(badFrames_path,'instance')

# move instance files from bad frames back into main frames

        root,_,pngfiles = next(os.walk(badFrames_instance_path))

        for png in pngfiles:
            png_path = os.path.join(root,png)
            # print "moved",png_path,"to",instance_path
            shutil.move(png_path, instance_path)

# # starting from 1.png, take n.png, and rename to (n-1).png
        instance_pngs = next(os.walk(instance_path))[2]

        if "0.png" in instance_pngs: instance_pngs.remove("0.png")

        for png in instance_pngs:
            old_frame_path = os.path.join(instance_path, png)
            temp_frame_path = os.path.join(instance_path, png + ".temp")
            shutil.move(old_frame_path, temp_frame_path)

        for png in instance_pngs:
            frameNum, ext = os.path.splitext(png)
            frameNum = int(frameNum)
            new_frameNum = frameNum - 1
            temp_frame_path = os.path.join(instance_path, png + ".temp")
            new_frame_path = os.path.join(instance_path, str(new_frameNum)+ext)
            shutil.move(temp_frame_path, new_frame_path)
            

# # identify last index of the set and remove the rgb and depth images of that last index,
# # remove 0.png of label and instance as well. 
        pngs = next(os.walk(instance_path))[2]
        frames = []
        for png in pngs:
            frame, ext = os.path.splitext(png)
            frames.append(int(frame))
            
        frames = list(set(frames))
        if frames:
            lastFrame = frames[-1] + 1
            lastFrame_depth_path = os.path.join(depth_path,str(lastFrame)+".png")
            # print "removed",lastFrame_depth_path
            removeIfExists(lastFrame_depth_path)
            lastFrame_rgb_path = os.path.join(rgb_path,str(lastFrame)+".jpg")
            # print "removed",lastFrame_rgb_path
            removeIfExists(lastFrame_rgb_path)
            lastFrame_depth_path = os.path.join(badFrames_depth_path,str(lastFrame)+".png")
            # print "removed",lastFrame_depth_path
            removeIfExists(lastFrame_depth_path)
            lastFrame_rgb_path = os.path.join(badFrames_rgb_path,str(lastFrame)+".jpg")
            # print "removed",lastFrame_rgb_path
            removeIfExists(lastFrame_rgb_path)

# # for each index in badFrames/photo, move the corresponding index images from instance and label
# # back into badFrames
        bad_pngs = next(os.walk(badFrames_depth_path))[2]

        for bad_png in bad_pngs:
            instance_bad_png_path = os.path.join(instance_path,bad_png)
            shutil.move(instance_bad_png_path, badFrames_instance_path)
            # print "moved",instance_bad_png_path,"to",badFrames_instance_path 


# # remove labels folder and run label script 
        if os.path.exists(labels_path): 
            shutil.rmtree(labels_path)
            # print "removed",labels_path

    instance2classFromInfoLog_scratch_outputs.main(house)