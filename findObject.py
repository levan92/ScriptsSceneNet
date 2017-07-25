import numpy as np
import sys
import os.path
from scipy import misc
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import time
from MinimumBoundingBox import minimum_bounding_box
import math

def findNeighbours(pixel, pixels_objects, neighbour_dist):
    object_group = []
    object_group.append(pixel)
    obj_loc = np.array(pixel)
    # obj_bb = [np.array(pixel),np.array(pixel)]
    surrounding = range(-neighbour_dist, neighbour_dist+1)
    for p in object_group:
        for neighbour in [(p[0]+i,p[1]+j) for i in surrounding for j in surrounding if (i != 0 or j != 0)]:
            if neighbour not in object_group and neighbour in pixels_objects:
                pixels_objects.remove(neighbour)
                object_group.append(neighbour)
                obj_loc += np.array(neighbour)
                # obj_bb[0][0] = min(obj_bb[0][0], neighbour[0])
                # obj_bb[0][1] = min(obj_bb[0][1], neighbour[1])
                # obj_bb[1][0] = max(obj_bb[1][0], neighbour[0])
                # obj_bb[1][1] = max(obj_bb[1][1], neighbour[1])             
    obj_loc = obj_loc / float(len(object_group))
    if len(object_group)>=3:
        min_bb_dict = minimum_bounding_box(object_group)
        obj_bb = list(min_bb_dict.corner_points)
        centroid = min_bb_dict.rectangle_center
        obj_bb.sort(key=lambda p: math.atan2(p[1]-centroid[1],p[0]-centroid[0]))
    else:
        obj_bb = object_group
    return object_group, obj_loc, obj_bb, pixels_objects

def main(pred_path):
    start = time.time()
    
    FG_threshold_i = 50 #anything higher than i = 50 will be ignored
    neighbour_dist = 1 # <= 2 tiles away is considered neighbour
    obj_min_size = 10 #needs to be more than this size to be considered obj
    
    pred_image = misc.imread(pred_path)
    # cropped_image = pred_image[FG_threshold_i:]
    height, width = np.shape(pred_image)
    pixels_objects = np.asarray(np.where(pred_image == 3)).T
    pixels_objects = [tuple(l) for l in pixels_objects]
    pixels_objects = [c for c in pixels_objects if c[0] > FG_threshold_i]
    objects = []
    objs_loc = []
    objs_bb = []
    for n, pixel in enumerate(pixels_objects):
        object_group, obj_loc, obj_bb, pixels_objects = \
            findNeighbours(pixel, pixels_objects, neighbour_dist)
        if len(object_group) >= obj_min_size:
            objects.append(object_group)
            objs_loc.append(obj_loc)
            objs_bb.append(obj_bb)
    print 'num of objects:',len(objects)
    print 'Duration:',time.time()-start,'sec.'
    axes = plt.gca()
    axes.set_xlim([0,width])
    axes.set_ylim([0,height])
    axes.invert_yaxis()
    for i in range(len(objects)):
        y,x = zip(*objects[i]) 
        plt.scatter(x=x, y=y,marker=".",s=3)
        plt.plot(objs_loc[i][1],objs_loc[i][0],'r.')
        obj_bb = objs_bb[i]
        obj_bb = [[point[1],point[0]] for point in obj_bb]
        axes.add_patch(plt.Polygon(obj_bb, closed=True, fill=None, edgecolor='r'))
        # min_bb = objs_bb[i][0]
        # max_bb = objs_bb[i][1]
        # axes.add_patch(Rectangle((min_bb[1],min_bb[0]),
        #                 max_bb[1] - min_bb[1],
        #                 max_bb[0] - min_bb[0], fc="none", ec='r'))
    savename = pred_path.replace('.png','_grouped.png')
    plt.savefig(savename)
    plt.show()

if __name__ == "__main__":
    main(os.path.normpath(sys.argv[1]))