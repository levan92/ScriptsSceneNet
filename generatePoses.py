import numpy as np
import pickle
import math

### Functions

#initialise poses.txt with default heading lines
def initPoseFile():
    w = open("poses.txt","w")
    w.write('#first three elements, eye and last three, lookAt\n')
    w.write('#frame rate\n')
    w.write('#shutter_speed\n') 
    return w

def robotOutOfRoom(pose, room):
    room = room + 1 # for loop iteration starts from 0 but ocMap starts from 1
    robotD_cell = int(math.ceil(robotD/cellSide))
    zx_start = pose[:2]
    zx = list(zx_start)

    for i in range(robotD_cell):
        for j in range(robotD_cell):
            cell = world2CellCoord(zx)
            if not (ocMap[cell[0]][cell[1]] == room):
                return True
            zx[1] += cellSide
        zx[1] = zx_start[1]
        zx[0] += cellSide
    
    return False

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

def world2CellCoord(world):
    [z,x] = world
    i = int( np.floor((z - origin_ocMap[0]) / cellSide) )
    j = int( np.floor((x - origin_ocMap[1]) / cellSide) )
    return np.array([i,j])

# def selectTurn():
#     if (turnToggle == 0): return -90 # turn right
#     else: return 90 # turn left 

### User variables
# robot parameters
robotD = 0.30 # diameter in m
robotR = robotD / 2. # radius
robotH = 0.20 # height in m
camDownAngle = 22.5 # in deg, angle camera looks down at
camForwardD = robotH / np.tan(np.deg2rad(camDownAngle))
robotV_straight = .3 # forward speed in m/s
robotV_turn = 45 # turning speed in deg/s
# simulation parameters
timeStep = 0.1 # simulation time step in sec
frameStep = 30 # capture a frame every [frameStep] timeSteps

### Main
f = open ('fromOcMap.pckl','rb')
[ocMap, numRooms, cellSide, origin_ocMap, floorHeight,
 roomsTopLeftCoord, roomsCentreCoord, roomsSize] = pickle.load(f)
f.close()

wf = initPoseFile()

framesCount = 0
for r in range(numRooms):
    print 'Rooms cleaned: ', r, '/', numRooms 
    #start with top left of each room, facing right
    topLeftCoord = cell2WorldCoord(roomsTopLeftCoord[r])
    pose = np.array([topLeftCoord[0],    #z
                     topLeftCoord[1],    #x
                     np.deg2rad(90)])  #theta
    i = 0
    turnToggle = -1 # first uturn is right, second is left, ...
    uturn = firstTurn = straight = secondTurn = finalStraightCheck = False
    uturnHitWallCount = 0
    uturnCount = 0
    while True:
        if not uturn:
            D = timeStep * robotV_straight
            newPose = getPose_straight(pose, D)
            if robotOutOfRoom(newPose, r):
                uturn = True 
                # print 'going to uturn'
                firstTurn = True
                totalTurn = 90 * turnToggle #turn right or left
            else: 
                pose = newPose
                # if i%50 == 0: print 'going straight'

        if uturn:
            if secondTurn:
                turnAngle = timeStep * robotV_turn * turnToggle
                if abs(turnAngle) < abs(totalTurn):
                    newPose = getPose_turn(pose, 0, turnAngle)
                    totalTurn = totalTurn - turnAngle 
                else: 
                    newPose = getPose_turn(pose, 0, totalTurn) 
                    secondTurn = False
                    uturn = False
                    # print 'uturn completed'
                    uturnCount += 1
                    turnToggle = -turnToggle

            elif straight:
                D = timeStep * robotV_straight
                if D < totalD:
                    newPose = getPose_straight(pose, D)
                    totalD = totalD - D
                else:
                    newPose = getPose_straight(pose, totalD)
                    straight = False
                    finalStraightCheck = True
                    # print 'uturn straight done'
                    secondTurn = True
                    totalTurn = 90 * turnToggle #turn right or left

            elif firstTurn:
                turnAngle = timeStep * robotV_turn * turnToggle
                if abs(turnAngle) < abs(totalTurn):
                    newPose = getPose_turn(pose, 0, turnAngle)
                    totalTurn = totalTurn - turnAngle 
                else: 
                    newPose = getPose_turn(pose, 0, totalTurn) 
                    firstTurn = False
                    # print 'firstTurn done'
                    straight = True
                    totalD = robotD

            # if robot going to exit room during uturn, 
            # throw away current new pose and 
            # immediately turn on the spot towards horizontal straight motion
            if robotOutOfRoom(newPose, r):
                firstTurn = straight = False
                secondTurn = True
                totalTurn = 90 * turnToggle
                uturnHitWallCount += 1
                # TODO: reset uturnHitWallCount everytime successful full uturn is done. 
                # print "uturnHitWallCount:", uturnHitWallCount
                if uturnHitWallCount >= 2: break
            else: 
                pose = newPose
                # if successfully completes the full straight motion during uturn, uturnHitWallCount is resetted
                if finalStraightCheck: uturnHitWallCount = 0

            finalStraightCheck = False

        if i%frameStep == 0:
            printPoseToFile(r, pose, wf)
            framesCount += 1

        i += 1;
    #end while true loop
    print "num uturns done for Room", r+1,":",uturnCount

print 'poses.txt generated, num of rooms:', numRooms, \
        ', total num frames:', framesCount









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
#                x_min + 0.05 + robotR,
#                np.deg2rad(90)])

# # i = 0
# t = 0
# n = 0
# turning = False
# while True:
#     # bearings3D = np.array([bearings[1], 0., bearings[0]])
#     # newRobotLoc = robotLoc + step * bearings3D
#     if turning:
#       deltaTheta = th * omega_turn
#       if abs(deltaTheta) > abs(targetDeltaTheta): 
#           deltaTheta = targetDeltaTheta
#           turning = False
#       else:
#           targetDeltaTheta -= deltaTheta
#       pose = getPose_turn(pose, R, deltaTheta)

#     else:
#           D = th * v_straight
#       pose = getPose_straight(pose, D)
#       if goingToHitWall(pose):
#           turning = True
#           targetDeltaTheta = 90

#     t += th









