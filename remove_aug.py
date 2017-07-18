import sys
import imgaug as ia
from imgaug import augmenters as iaa
import pathlib
import cv2
import numpy as np
import os

def get_item_paths(path):
    items = []
    for p in pathlib.Path(path).iterdir():
        # if str(p).endswith('_rgb.jpg') and 'aug_rgb' not in str(p):
        if str(p).endswith('_rgb.jpg'):
            depth_path = str(p).replace('_rgb.jpg','_depth.png')
            if not os.path.exists(depth_path): 
                print depth_path,'does not exist.'
                depth_path = ''
            label_path = str(p).replace('_rgb.jpg','_label.png')
            if not os.path.exists(label_path): 
                print label_path,'does not exist.'
                label_path = ''
            items.append({'image':str(p), 
                          'depth':depth_path, 
                          'label':label_path })
    return items

def main(dataset_dir):
    item_paths = get_item_paths(dataset_dir) 

    for root, directories, files in os.walk(dataset_dir):
        for file in files:
            if "aug" in file:
                path = os.path.join(root, file)
                os.unlink(os.path.join(root, file))
                print "Removed",path
    
if __name__ == '__main__':
    main(sys.argv[1])
