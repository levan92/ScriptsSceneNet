import re 
import numpy as np
import pickle

#user variables
numOfFrames = 150
layoutDirectory='/homes/el216/Workspace/SceneNetData/Layouts'
layoutFile='/suncg_houses/house2.obj'
layoutFilePath = layoutDirectory+layoutFile
#robot parameters
robotD = 0.30 # diameter in m
robotR = robotD / 2. # radius
robotH = 0.20 # height in m
camDownAngle = 22.5 # in deg, angle camera looks down at
camForwardD = robotH / np.tan(camDownAngle/180.0*np.pi)
v_straight = 0.2 # speed when going straight in m/s
omega_turn = 90 # turn speed in deg/s
#simulation parameters
th = 0.05 # time step
frameStep = 1 # extract frame every frameStep secs

# step = 0.01 # movement simulation stepsize in m

#check if robot location is valid
def valid(robotLoc, bearings3D):
    # lookAtLoc = robotLoc + (robotR + camForwardD) * bearings3D
    camLoc = robotLoc + robotR * bearings3D \
                      + np.array([0.,robotH,0.])
    buffer = 0.1 #10cm buffer
    if ( (x_min+buffer<camLoc[0]<x_max-buffer) and 
         (z_min+buffer<camLoc[2]<z_max-buffer) ): return True
    return False

#prints camera and look at points to file
def printPointsToFile(iteration, robotLoc, bearings3D, file):
    camLoc = robotLoc + robotR * bearings3D \
                      + np.array([0.,robotH,0.])
    lookAtLoc = robotLoc + (robotR + camForwardD) * bearings3D
    print >> file, iteration, \
             camLoc[0], camLoc[1], camLoc[2], \
             lookAtLoc[0], lookAtLoc[1], lookAtLoc[2]
    print >> file, iteration, \
             camLoc[0], camLoc[1], camLoc[2], \
             lookAtLoc[0], lookAtLoc[1], lookAtLoc[2]

#turns bearings right by 90 degrees
def turnRight90 (bearings):
    print 'turned right'
    bearings = np.dot(np.array([[0,1],[-1,0]]), bearings)
    return bearings

#theta in rads, negative theta to turn right
def turnLeftTheta (bearings, theta):
    print 'turned by',theta
    bearings = np.dot(np.array([[np.cos(theta),-np.sin(theta)],
                                [np.sin(theta),np.cos(theta)]]), bearings)
    return bearings/np.linalg.norm(bearings)

def goingToHitWall(pose):

	return

# D in m
def getPose_straight(pose, D):
	newPose[0] = pose[0] + D * np.cos(pose[2])
	newPose[1] = pose[1] + D * np.sin(pose[2])
	newPose[2] = pose[2]
	return newPose

# R in m, deltaTheta in deg
def getPose_turn(pose, R, deltaTheta): 
	deltaTheta_rad = np.deg2rad(deltaTheta)
	newPose[0] = pose[0] + R * ( np.sin(pose[2] + deltaTheta_rad) - sin(deltaTheta_rad) )
	newPose[1] = pose[1] - R * ( np.cos(pose[2] + deltaTheta_rad) - cos(deltaTheta_rad) )
	newPose[2] = pose[2] + deltaTheta_rad
	return newPose

# wraps angle within -pi and pi
def wrap (angle):
	while (angle <= -np.pi): angle += 2 * np.pi
	while (angle > np.pi): angle -= 2 * np.pi
	return angle

def listOflist(size):
    listOflist = list()
    for i in range(0,size):
        listOflist.append( list() )
    return listOflist

def getRoomsInfo(ocMap, numRooms, cellSide):
    roomsTopLeftCoord = np.empty((numRooms,2))
    roomsTopLeftCoord[:] = np.NAN
    roomsCoords = listOflist(numRooms)
    for i,row in enumerate(ocMap):
        for j,roomIdx in enumerate(row):
            if not roomIdx == 0.:
                roomIdx = int(roomIdx-1)

                if np.isnan(roomsTopLeftCoord[roomIdx][0]):
                    roomsTopLeftCoord[roomIdx] = [i,j]
                
                roomsCoords[roomIdx].extend([i,j])

    roomsCoords = np.array(roomsCoords)    
    roomsCentreCoord = np.zeros((numRooms,2))
    for i in range(numRooms):
        roomCoords = roomsCoords[i]
        i_coords = [k for k in roomCoords if k % 2 == 0]
        if (i == 0):
            print roomCoords
            print '\n'
            print i_coords


        length = len(roomCoords)
        centre = length / 2 # integer division

    return roomsTopLeftCoord, roomsCoords


f = open ('fromOcMap.pckl','rb')
[ocMap, numRooms, cellSide] = pickle.load(f)
f.close()

roomsTopLeftCoord, roomsCoords = getRoomsInfo(ocMap, numRooms, cellSide)













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









