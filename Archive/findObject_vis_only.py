import numpy as np
import os.path
from scipy.misc import imread
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.cm as cm
import time
from MinimumBoundingBox import minimum_bounding_box
from math import atan2
import argparse
import linecache

def findNeighbours(pixel, pixels_objects, neighbour_dist, obj_min_size, min_filled_ratio):
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
    if len(object_group) >= obj_min_size:
        min_bb_dict = minimum_bounding_box(object_group)
        obj_bb = list(min_bb_dict.corner_points)
        centroid = min_bb_dict.rectangle_center
        obj_bb.sort(key=lambda p: atan2(p[1]-centroid[1],p[0]-centroid[0]))
        # if (len(object_group) / min_bb_dict.area) > min_filled_ratio:
        return object_group, obj_loc, obj_bb, pixels_objects
    object_group = None
    obj_loc = None
    obj_bb = None
    return object_group, obj_loc, obj_bb, pixels_objects
    

def getWorldLoc(obj_loc_pix, cam_pose, cam_info, floorHeight, image_size):
    # cam_pose: x, y, z, theta(about y), look-down angle
    # cam_info: hFoV, vFoV, focal length
    hFoV, vFoV, f_l = cam_info
    height_pix, width_pix = image_size
    scaling = np.tan(np.deg2rad(hFoV/2.0)) * f_l * 2 / width_pix 
    scaling = np.tan(np.deg2rad(vFoV/2.0)) * f_l * 2 / height_pix 
    y_c = (height_pix/2.0 - obj_loc_pix[0]) * scaling
    x_c = (width_pix/2.0 - obj_loc_pix[1]) * scaling
    p_c = np.array([x_c, y_c, f_l])
    cam_x, cam_y, cam_z, theta, alpha = cam_pose
    # R_wc = np.array([
    # [np.cos(theta), 0, np.sin(theta)],
    # [np.sin(alpha)*np.sin(theta), np.cos(alpha), -np.sin(alpha)*np.cos(theta)],
    # [-np.cos(alpha)*np.sin(theta), np.sin(alpha), np.cos(alpha)*np.cos(theta)]
    #                  ])
    R_alpha = np.array([[1,0,0],
                        [0,np.cos(alpha),-np.sin(alpha)],
                        [0,np.sin(alpha),np.cos(alpha)]
                        ])
    R_theta = np.array([[np.cos(theta), 0, np.sin(theta)],
                        [0,1,0],
                        [-np.sin(theta), 0, np.cos(theta)]
                        ])
    p_c2 = np.dot(R_alpha,p_c)
    p_w = np.dot(R_theta, p_c2)
    p_0_w = np.array([cam_x, cam_y, cam_z])
    mu = (floorHeight - p_0_w[1]) / p_w[1]
    obj_loc_w_zx = np.array([p_0_w[2] + mu * p_w[2],  #z
                             p_0_w[0] + mu * p_w[0]]) #x
    return obj_loc_w_zx

def main(pred_path):
    start = time.time()

    FG_threshold_i = 90 #anything higher than i = 50 will be ignored
    neighbour_dist = 1 # <= 2 tiles away is considered neighbour
    # obj_min_size = 150 #needs to be more than this size to be considered obj
    obj_min_size = 250 #needs to be more than this size to be considered obj
    # w.r.t. to a 240 x 320 label png
    min_filled_ratio = 0.5 #object's pixels need to fill up more than [ratio] of its bounding box

    pred_image = imread(pred_path)
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
            findNeighbours(pixel, pixels_objects, neighbour_dist, obj_min_size, min_filled_ratio)
        if object_group:
            objects.append(object_group)
            objs_loc.append(obj_loc)
            objs_bb.append(obj_bb)
    print 'num of objects:',len(objects)
    print 'Duration:',time.time()-start,'sec.'
    axes = plt.gca()
    axes.set_xlim([0,width])
    axes.set_ylim([0,height])
    axes.invert_yaxis()
    colors = cm.jet(np.linspace(0,1,len(objects)))
    for i in range(len(objects)):
        # print objs_loc[i]
        y,x = zip(*objects[i]) 
        plt.scatter(x=x, y=y,marker=".",s=3, color=colors[i])
        plt.plot(objs_loc[i][1],objs_loc[i][0],'r.')
        obj_bb = objs_bb[i]
        obj_bb = [[point[1],point[0]] for point in obj_bb]
        axes.add_patch(plt.Polygon(obj_bb, closed=True, fill=None, edgecolor='r'))
    savename = pred_path.replace('.png','_grouped.png')
    plt.savefig(savename)
    # plt.show()
    plt.clf()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('pred_path', help='path to image to find objects', 
                        type=str)
    args = parser.parse_args()
    main(os.path.normpath(args.pred_path))