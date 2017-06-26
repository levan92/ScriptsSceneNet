import json
import numpy as np
import sys

houseID = str(sys.argv[1])
lighting_info_file='/homes/el216/Workspace/SUNCGtoolbox/metadata/suncgModelLights.json'
# house_folder="/homes/el216/Workspace/OutputSceneNet/fe3649f602f371d76660b5cb7219c3d0_badLighting"
# house_folder="/scratch/el216/suncg/house/7bee7018f8b103d2cb1e4c63202a8a52/"
house_folder="/homes/el216/Workspace/OutputSceneNet/7bee7018f8b103d2cb1e4c63202a8a52_badLighting"

house_folder = "/scratch/el216/suncg/house/" + houseID

lighting_json = json.loads(open(lighting_info_file).read())
lights_modelID = lighting_json.keys()

json_filepath= house_folder + '/house.json'
json_file = open(json_filepath)
json_str = json_file.read()
house_data = json.loads(json_str)
nodes_list = house_data['levels'][0]['nodes']

room_count = 0

for node in nodes_list:
    print node['id'], node['type'], node['modelId']
    if node['type'] == "Room":
        room_count += 1



    if node['type'] == "Object":
        if node['modelId'] in lights_modelID:
            a = 1
            # print node['id'], node['modelId']


# for lighting_group in lighting_json:
#     for light in lighting_group:
#         if light['type'] == "SpotLight":



# point_light power rgb pos(xyz) radius
# spot_light  power rgb pos(xyz) v1 v2 ()
