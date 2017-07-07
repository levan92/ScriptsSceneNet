from scipy import misc
import matplotlib.pyplot as plt
import sys
import os

impath = sys.argv[1]

fullname = os.path.basename(impath)
[basename,ext] = os.path.splitext(impath)

image = misc.imread(impath)
plt.imshow(image,interpolation='nearest')
plt.colorbar()
plt.savefig(basename + "_vis" + ext)

plt.clf()