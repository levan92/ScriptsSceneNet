import re 
import numpy as np
import pickle

### Functions

#initialise poses.txt with default heading lines
def initPoseFile():
    w = open("poses.txt","w")
    w.write('#first three elements, eye and last three, lookAt\n')
    w.write('#frame rate\n')
    w.write('#shutter_speed\n') 
    return w

#check if robot location is valid
def valid(robotLoc, bearings3D):
    return

#prints camera and look at points to file
def printPoseToFile(index, pose, file):
    camLoc = np.zeros(3)
    lookAtLoc = np.zeros(3)
    # x
    camLoc[0] = pose[1] + robotR * np.sin(pose[2])
    lookAtLoc[0] = pose[1] + (robotR+camForwardD) * np.sin(pose[2])
    # y
    camLoc[1] = floorHeight + robotH
    lookAtLoc[1] = floorHeight
    # z
    camLoc[2] = pose[0] + robotR * np.cos(pose[2])
    lookAtLoc[2] = pose[0] + (robotR+camForwardD) * np.cos(pose[2])

    print >> file, index, \
             camLoc[0], camLoc[1], camLoc[2], \
             lookAtLoc[0], lookAtLoc[1], lookAtLoc[2]
    print >> file, index, \
             camLoc[0], camLoc[1], camLoc[2], \
             lookAtLoc[0], lookAtLoc[1], lookAtLoc[2]

def goingToHitWall(pose):

	return

# D in m
def getPose_straight(pose, D):
    newPose = np.zeros(3)
    newPose[0] = pose[0] + D * np.cos(pose[2])
    newPose[1] = pose[1] + D * np.sin(pose[2])
    newPose[2] = pose[2]
    return newPose

# wraps angle within -pi and pi
def wrap (rad):
    while (rad <= -np.pi): rad += 2 * np.pi
    while (rad > np.pi): rad -= 2 * np.pi
    return rad

# R in m, deltaTheta in deg
def getPose_turn(pose, R, deltaTheta): 
    newPose = np.zeros(3)
    deltaTheta_rad = np.deg2rad(deltaTheta)
    #z
    newPose[0] = pose[0] + R * ( np.sin(pose[2] + deltaTheta_rad) \
                 - np.sin(deltaTheta_rad) )
    #x
    newPose[1] = pose[1] - R * ( np.cos(pose[2] + deltaTheta_rad) \
                 - np.cos(deltaTheta_rad) )
    #theta
    newPose[2] = wrap(pose[2] + deltaTheta_rad)
    return newPose

def cell2WorldCoord(cell):
    [i,j] = cell
    z = origin_ocMap[0] + cellSide * (i + 0.5)
    x = origin_ocMap[1] + cellSide * (j + 0.5)
    return np.array([z,x])

### User variables
framesPerRoom = 36
#robot parameters
robotD = 0.30 # diameter in m
robotR = robotD / 2. # radius
robotH = 0.20 # height in m
camDownAngle = 22.5 # in deg, angle camera looks down at
camForwardD = robotH / np.tan(np.deg2rad(camDownAngle))

### Main

f = open ('fromOcMap.pckl','rb')
[ocMap, numRooms, cellSide, origin_ocMap, floorHeight,
 roomsTopLeftCoord, roomsCentreCoord, roomsSize] = pickle.load(f)
f.close()

wf = initPoseFile()

for r in range(numRooms):
    #start with centre of each room
    centreCoord = cell2WorldCoord(roomsCentreCoord[r])
    pose = np.array([centreCoord[0],    #z
                     centreCoord[1],    #x
                     np.deg2rad(180)])  #theta
    
    for i in range(framesPerRoom - 1):
        printPoseToFile(r, pose, wf)
        deltaTheta = 360 / framesPerRoom
        pose = getPose_turn(pose, 0, deltaTheta) # turning on the spot

print 'poses.txt generated, num of rooms:', numRooms, \
        ', floor height:', floorHeight, \
        ', total num frames:', (framesPerRoom * numRooms)



# #read layout file 
# x_min, x_max, y_min, y_max, z_min, z_max = getFloorBounds(layoutFilePath)

# print x_min, x_max, y_min, y_max, z_min, z_max

# # #hardcoding for office1_layout.obj
# # x_max = x_max - 0.6

# #write poses.txt
# w = open("poses.txt","w")
# w.write('#time, cameraPoint (3D), lookAtPoint (3D)\n')
# w.write('#frame rate per second: 25\n')
# w.write('#shutter_speed (s): 0.0166667\n') 

# # robotLoc = np.array([x_min + robotR + 1., y_min, z_min + robotR + 0.5])
# # bearings = np.array([0, 1]) #always unit vector, 2D (z & x axes) 

# # Initial pose
# pose = np.array([z_min + 0.05 + robotR,
# 				 x_min + 0.05 + robotR,
# 				 np.deg2rad(90)])

# # i = 0
# t = 0
# n = 0
# turning = False
# while True:
#     # bearings3D = np.array([bearings[1], 0., bearings[0]])
#     # newRobotLoc = robotLoc + step * bearings3D
#     if turning:
#     	deltaTheta = th * omega_turn
# 	   	if abs(deltaTheta) > abs(targetDeltaTheta): 
# 	   		deltaTheta = targetDeltaTheta
# 	   		turning = False
# 	   	else:
# 		   	targetDeltaTheta -= deltaTheta
#     	pose = getPose_turn(pose, R, deltaTheta)

#     else:
#    	    D = th * v_straight
#     	pose = getPose_straight(pose, D)
#     	if goingToHitWall(pose):
#     		turning = True
#     		targetDeltaTheta = 90

#     t += th









