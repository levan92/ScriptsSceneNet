import sys

housePath = sys.argv[1]

old = open(housePath + '/house.obj','r')
new = open(housePath + '/houseOneFloor.obj','w')

# inFloor = inCeiling = inWall = inObject = False
# wnidList = [] 
# textures = 0
# textureLists = []

for line in old:
	if line.startswith('g Level#1'): break
	new.write(line)

print 'Wrote new obj file to ', housePath + '/houseOneFloor.obj'