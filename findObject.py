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
        obj_bb.sort(key=lambda p: atan2(p[1]-centroid[1],p[0]-centroid[0]))
    else:
        obj_bb = object_group
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

def main(pred_path, cam_info_txt):
    start = time.time()
    
    FG_threshold_i = 50 #anything higher than i = 50 will be ignored
    neighbour_dist = 1 # <= 2 tiles away is considered neighbour
    obj_min_size = 10 #needs to be more than this size to be considered obj
    
    # Cam and Pose info
    cam_info = [float(i) for i in linecache.getline(cam_info_txt,1).split()]
    cam_pose = [float(i) for i in linecache.getline(cam_info_txt,2).split()]
    # cam_info = [56.144973871705915, 43.60281897270362, 0.20]
    #             #hFoV, vFoV, focal length (m?)
    floorHeight = 0.05 
    # robotH = 0.2
    # lookdown_angle = np.deg2rad(22.5)
    # cam_pose = np.array([0.,                    #x
    #                      floorHeight + robotH,  #y
    #                      0.,                    #z
    #                      np.deg2rad(90),   #facing direction
    #                      lookdown_angle])  #look-down angle
    print 'Current Coord(zx) of cam:','[',cam_pose[2],',',cam_pose[0],']'
    print 'facing',np.rad2deg(cam_pose[3]),'deg'
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
    colors = cm.jet(np.linspace(0,1,len(objects)))
    for i in range(len(objects)):
        # print objs_loc[i]
        y,x = zip(*objects[i]) 
        plt.scatter(x=x, y=y,marker=".",s=3, color=colors[i])
        plt.plot(objs_loc[i][1],objs_loc[i][0],'r.')
        obj_bb = objs_bb[i]
        obj_bb = [[point[1],point[0]] for point in obj_bb]
        axes.add_patch(plt.Polygon(obj_bb, closed=True, fill=None, edgecolor='r'))
        obj_loc_zx = getWorldLoc(objs_loc[i], cam_pose, cam_info, floorHeight, [height, width])
        print 'Coord(zx) of object in room:',obj_loc_zx

    savename = pred_path.replace('.png','_grouped.png')
    plt.savefig(savename)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('pred_path', help='path to image to find objects', 
                        type=str)
    parser.add_argument('cam_info_txt', help='corresponding camInfo.txt to frame',
                        type=str)
    args = parser.parse_args()
    main(os.path.normpath(args.pred_path), os.path.normpath(args.cam_info_txt))