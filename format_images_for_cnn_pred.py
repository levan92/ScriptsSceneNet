import os
import sys
import glob
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='directory of images')
    args = parser.parse_args()

    dir = os.path.normpath(args.dir)
    for image in os.scandir(dir):
        if image.name.endswith('_rgb.jpg'):
            print(image.name,'already right format')
        else:
            image = str(image.path)
            image_name = (os.path.splitext(image))[0]
            new_name = image_name + '_rgb.jpg'
            print("Renaming from",image,'to',new_name)
            os.rename(image, new_name)

