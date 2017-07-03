import json
import numpy as np
import sys
import pickle

num_houses_wanted = 100

lighting_info_file='/homes/el216/Workspace/SUNCGtoolbox/metadata/suncgModelLights.json'
lighting_json = json.loads(open(lighting_info_file).read())
lights_modelID = lighting_json.keys()

all_houses_file = open("all_houseIDs.txt",'rb')
houses_with_lights = []
houses_with_lights_file = open("all_houses_with_lights.txt",'wb')
h = 0
i = 0
for house in all_houses_file:
    house = house[:-1]
    house_folder = "/scratch/el216/suncg/house/" + house
    json_filepath= house_folder + '/house.json'
    json_file = open(json_filepath)
    json_str = json_file.read()
    house_data = json.loads(json_str)
    nodes_list = house_data['levels'][0]['nodes']

    rooms_with_light = []
    room_count = 0
    rooms_node_indices = []

    for node in nodes_list:
        if node['type'] == "Room":
            room_count += 1
            if 'nodeIndices' in node:
                rooms_node_indices.append(node['nodeIndices'])
            else:
                rooms_node_indices.append([])

    # the nodes for loops separated to make sure rooms are processed first then lighting.
    for node in nodes_list:
        if node['type'] == "Object":
            if node['modelId'] in lights_modelID:
                # print node['id'], node['modelId']
                lighting_group = lighting_json[node['modelId']]
                for r in range(room_count):
                    node_indices = rooms_node_indices[r]
                    node_id = int(node['id'].split('_')[1])
                    if node_id in node_indices:
                        rooms_with_light.append((r+1)) 

    if rooms_with_light: 
        # houses_with_lights.append(house)
        print >> houses_with_lights_file, house
        h += 1
        # print h

    # i += 1
    # if h >= num_houses_wanted: break

all_houses_file.close()
houses_with_lights_file.close()
print h
# print houses_with_lights