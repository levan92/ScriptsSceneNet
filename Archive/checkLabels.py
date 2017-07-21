import os
import sys
import numpy as np
import pathlib
from PIL import Image
import itertools

def main(dataset_dir):
    txt = open("labels_with_unknown.txt","w")
    # root, _ ,files = next(os.walk(dataset_dir))
    i = 0
    for file in pathlib.Path(dataset_dir).iterdir():
        file = str(file)
        basename = os.path.basename(file)
        if file.endswith('_label.png'):
            im = Image.open(file)
            pix = im.load()
            width, height = im.size
            for x,y in itertools.product(range(width),range(height)):
            # for x in range(width):
            #     for y in range(height):
                    if pix[x,y] == 0:
                        print >> txt, basename
                        print basename
                        break

            # image = cv2.imread(file)
            # print image[20,20]
            # for index, pixel in np.ndenumerate(image):
            #     print pixel
            #     if pixel == 0:
            #         print >> txt, basename
            #         print basename
            #         break
    txt.close()

if __name__ == "__main__":
    main(os.path.normpath(sys.argv[1]))