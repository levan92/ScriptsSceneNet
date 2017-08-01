import os
import sys
import glob

def main(dir):
    for image in os.scandir(dir):
        image = str(image.path)
        image_name = (os.path.splitext(image))[0]
        new_name = image_name + '_rgb.jpg'
        print("Renaming from",image,'to',new_name)
        os.rename(image, new_name)

if __name__ == "__main__":
    main(os.path.normpath(sys.argv[1]))