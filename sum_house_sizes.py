import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('houses_in_set', type=str, nargs='+', 
                    help='houses whose sizes is to be summed up')
args = parser.parse_args()
houses_in_set = args.houses_in_set

f = open('houses_overview.txt','r')
f.readline()
f.readline()
houses = []
sizes = []
for line in iter(f):
    if line.startswith('Unallocated'):
        continue
    house, size = line.split()
    houses.append(house)
    sizes.append(int(size))
f.close()
print (houses)
print (sizes)
sum = 0
for house in houses_in_set:
    sum += sizes[houses.index(house)]
print (sum)