import sys
import re
import numpy as np

layoutFileName = sys.argv[1]
r = open(layoutFileName,'r')
init = True
for line in r:
    if 'v ' in line:
        numStr = re.findall(r"[-+]?\d*\.\d+|\d+",line)
        vec3 = np.array([float(numStr[0]), float(numStr[1]), 
                         float(numStr[2])])
        if init:
            x_min = vec3[0]
            x_max = vec3[0]
            y_min = vec3[1]
            y_max = vec3[1]
            z_min = vec3[2]
            z_max = vec3[2]
            init = False
        else:
            if vec3[0] < x_min: x_min = vec3[0]
            if vec3[0] > x_max: x_max = vec3[0]
            if vec3[1] < y_min: y_min = vec3[1]
            if vec3[1] > y_max: y_max = vec3[1]
            if vec3[2] < z_min: z_min = vec3[2]
            if vec3[2] > z_max: z_max = vec3[2]

print 'x:', x_min, x_max, 'y:', y_min, y_max, 'z:', z_min, z_max