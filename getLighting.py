import json
import numpy as np
import sys

houseID = str(sys.argv[1])
lighting_info_file='/homes/el216/Workspace/SUNCGtoolbox/metadata/suncgModelLights.json'

pointLight_rad = 0.05
spotLight_side = 0.1
lineLight_width = 0.03


def light_pos_from_trans(transform, local_pos):
    T_mat = np.zeros([4,4])
    T_mat[:,0] = transform[0:4]
    T_mat[:,1] = transform[4:8]
    T_mat[:,2] = transform[8:12]
    T_mat[:,3] = transform[12:16]
    local_pos_np = np.append(np.array(local_pos),1.0)
    pos = np.dot(T_mat,local_pos_np)[0:3]
    # print T_mat, local_pos_np, pos
    return pos


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

rooms_with_light = []
room_count = 0
rooms_node_indices = []

lights_info = []

for node in nodes_list:
    # print node['id'], node['type'], node['modelId']
    if node['type'] == "Room":
        room_count += 1
        rooms_node_indices.append(node['nodeIndices'])

    if node['type'] == "Object":
        if node['modelId'] in lights_modelID:
            # print node['id'], node['modelId']
            lighting_group = lighting_json[node['modelId']]
            for light in lighting_group:
                color_hex = light['color'].lstrip('#')
                color_dec = tuple(int(color_hex[i:i+2],16) for i in (0,2,4))
                color_norm = tuple([x/255 for x in color_dec])

                if light['type'] == 'PointLight':                  
                    pos = light_pos_from_trans(node['transform'],light['position'])
                    pos_string = ' '.join(str(i) for i in pos)
                    
                    line_info = light['type'] + ' ' + str(light['power']) + \
                                ' ' + str(color_norm)  + ' ' + pos_string + \
                                ' ' + str(pointLight_rad) 
                    # print line_info

                elif light['type'] == 'SpotLight':
                    pos_centre = light_pos_from_trans(node['transform'],light['position'])
                    pos_corner = pos_centre - np.array([-spotLight_side, 0., spotLight_side])
                    v_x = np.array([spotLight_side,0.,0.])
                    v_z = np.array([0.,0.,-spotLight_side])
                    
                    pos_corner_str = ' '.join(str(i) for i in pos_corner)
                    v_x_str = ' '.join(str(i) for i in v_x)
                    v_z_str = ' '.join(str(i) for i in v_z)

                    line_info = light['type'] + ' ' + str(light['power']) + \
                                ' ' + str(color_norm)  + ' ' + pos_corner_str + \
                                ' ' + v_x_str + ' ' +  v_z_str
                    # print line_info

                elif light['type'] == 'LineLight': #LineLights are modelled as SpotLights
                    pos1 = light_pos_from_trans(node['transform'],light['position'])
                    pos2 = light_pos_from_trans(node['transform'],light['position2'])
                    v1 = pos2 - pos1
                    v2_x = np.sqrt( lineLight_width**2 / (1 + (v1[0]/v1[2])**2) )
                    v2_z = - v2_x * v1[0] / v1[2]
                    v2 = np.array([v2_x, 0., v2_z])
                    pos_corner = pos1 - v2/2.

                    pos_corner_str = ' '.join(str(i) for i in pos_corner)
                    v1_str = ' '.join(str(i) for i in v1)
                    v2_str = ' '.join(str(i) for i in v2)

                    print 'LINELIGHT', pos1, pos2, v1, v2, pos_corner

                    line_info = light['type'] + ' ' + str(light['power']) + \
                                ' ' + str(color_norm)  + ' ' + pos_string + \
                                ' ' + "0.1"  
                    # print line_info


            for r in range(room_count):
                node_indices = rooms_node_indices[r]
                if int(node['id'].split('_')[1]) in node_indices:
                    rooms_with_light.append(r) 

rooms_with_light = set(rooms_with_light) #room index starts from 0 (NOT 1)


pos1 = np.array([10.,10.,10.])
pos2 = np.array([20.,20.,20.])
v1 = pos2 - pos1
v2_x = np.sqrt( lineLight_width**2 / (1 + (v1[0]/v1[2])**2) )
v2_z = - v2_x * v1[0] / v1[2]
v2 = np.array([v2_x, 0., v2_z])
pos_corner = pos1 - v2/2.

print 'LINELIGHT', pos1, pos2, v1, v2, pos_corner



# PointLight power rgb pos(xyz) radius
# SpotLight/LineLight  power rgb pos(xyz) v1 v2 ()
