import numpy as np
import pickle
import math
from pylab import *
np.set_printoptions(threshold=np.nan)

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
    robotD_cell = int(math.ceil(robotD/cellSide)) + 1
    zx_start = [pose[0]-robotR, pose[1]-robotR] #top-left corner of robot bb
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

def visualiseScanning(poses_cell):
    fig, ax = plt.subplots()

    # define the colormap
    cmap = plt.cm.jet
    cmaplist = [cmap(i) for i in range(cmap.N)]
    cmaplist[0] = (.5,.5,.5,1.0)
    cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)

    bounds = np.linspace(0,numRooms+1,numRooms+2)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    img = ax.imshow(ocMap,interpolation='nearest',cmap=cmap, norm=norm)
    poses_cell = np.array(poses_cell)
    x = poses_cell[:,1]
    # print x
    y = poses_cell[:,0]
    # print y
    plt.plot(x, y,'r-')

    plt.colorbar(img, cmap=cmap, norm=norm, spacing='proportional', 
                    ticks=bounds, boundaries=bounds, format='%1i')
    ax.set_title('Scanning pattern')
    savefig('scanningPatternDemo.png')
    show()
    return

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
# capture a frame every [frameStep] timeSteps
# frameStep = 20 
frameStep = sys.argv[1]

### Main
f = open ('fromOcMap.pckl','rb')
[ocMap, numRooms, cellSide, origin_ocMap, floorHeight,
              roomsBBmin, roomsBBmax, roomsSize] = pickle.load(f)
f.close()

wf = initPoseFile()

poses_cell = []

framesCountTotal = 0
for r in range(numRooms):

    if ( (roomsSize[r]*cellSide) < robotD ).any():
        print 'Room ', r,'too small, skipping..'
        continue

    print 'Cleaning Room: ', r, '/', numRooms 
    #start with top left of each room, facing right
    topLeftCoord = cell2WorldCoord(roomsBBmin[r])
    pose = np.array([topLeftCoord[0] + robotR,    #z
                     topLeftCoord[1] + robotR,    #x
                     np.deg2rad(90)])  #theta
    
    while robotOutOfRoom(pose,r):
        pose = pose + np.array([cellSide, 0, 0])

    i = 0
    turnToggle = -1 # first uturn is right, second is left, ...
    uturn = firstTurn = straight = secondTurn = finalStraightCheck = False
    uturnHitWallCount = 0
    uturnCount = 0
    framesCountRoom = 0
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
                # print "uturnHitWallCount:", uturnHitWallCount
                if uturnHitWallCount >= 2: break
            else: 
                pose = newPose
                # if successfully completes the full straight motion during uturn, uturnHitWallCount is resetted

                if finalStraightCheck: 
                    uturnHitWallCount = 0
                    # print 'uturn straight done'

            finalStraightCheck = False

        if i%frameStep == 0:
            printPoseToFile(r, pose, wf)
            framesCountRoom += 1

        i += 1;
        poses_cell.append(world2CellCoord(pose[:2]))


    #end while true loop
    # print "num uturns done for Room", r+1,":",uturnCount
    print "frames generated for Room", r,":",framesCountRoom
    framesCountTotal += framesCountRoom



print 'poses.txt generated, num of rooms:', numRooms, \
        ', total num frames:', framesCountTotal

# visualiseScanning(poses_cell)







