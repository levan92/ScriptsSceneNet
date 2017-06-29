import json
import numpy as np
import sys
import pickle

houseID = str(sys.argv[1])
house_temp_dir = '/homes/el216/Workspace/ScriptsSceneNet/' + houseID + '/'
lighting_info_file='/homes/el216/Workspace/SUNCGtoolbox/metadata/suncgModelLights.json'

pointLight_rad = 0.02
spotLight_side = 0.04
lineLight_width = 0.01
pow_scaling_factor = float(sys.argv[2])

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

lighting_log_file = house_temp_dir + houseID + '_lighting.txt'
log = open(lighting_log_file,'wb')

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

for node in nodes_list:
    # print node['id'], node['type'], node['modelId']
    if node['type'] == "Room":
        # print room_count+1, node['id']
        room_count += 1
        if 'nodeIndices' in node:
            rooms_node_indices.append(node['nodeIndices'])
        else:
            rooms_node_indices.append([])

lights_info = []
light_index = 0
lights_in_rooms_byNodeID = [[] for i in range(room_count)]
lights_in_rooms_byIndex = [[] for i in range(room_count)]
light_index_list = []

# the nodes for loops separated to make sure rooms are processed first then lighting.
for node in nodes_list:
    if node['type'] == "Object":
        if node['modelId'] in lights_modelID:
            # print node['id'], node['modelId']
            lighting_group = lighting_json[node['modelId']]
            for light in lighting_group:
                color_hex = light['color'].lstrip('#')
                color_dec = tuple(int(color_hex[i:i+2],16) for i in (0,2,4))
                color_norm = tuple([x/255 for x in color_dec])
                color_str = ' '.join(str(i) for i in color_norm)

                power = pow_scaling_factor * light['power']
                power_str = str(power)

                if light['type'] == 'PointLight':                  
                    pos = light_pos_from_trans(node['transform'],light['position'])
                    pos_string = ' '.join(str(i) for i in pos)
                    
                    line_info = str(light['type']) + ' ' + power_str + \
                                ' ' + color_str  + ' ' + pos_string + \
                                ' ' + str(pointLight_rad) 

                elif light['type'] == 'SpotLight':
                    # if light['direction'][1] >= 0:
                    #     continue                 
                    d = np.array(light['direction'])

                    if d[0] == 0.:
                        v1_unscaled = np.array([1., 0., 0.])
                    else:
                        v1_unscaled = np.array([-d[2]/d[0], 0., 1.])
    
                    v2_unscaled = np.cross(d,v1_unscaled)

                    v1 = (spotLight_side/np.linalg.norm(v1_unscaled)) * v1_unscaled
                    v2 = (spotLight_side/np.linalg.norm(v2_unscaled)) * v2_unscaled

                    pos_centre = light_pos_from_trans(node['transform'],light['position'])
                    pos_corner = pos_centre - 0.5 * v1 - 0.5 * v2

                    # v_1 = np.array([0.,0.,-spotLight_side])
                    # v_2 = np.array([spotLight_side,0.,0.])
                    
                    pos_corner_str = ' '.join(str(i) for i in pos_corner)
                    v1_str = ' '.join(str(i) for i in v1)
                    v2_str = ' '.join(str(i) for i in v2)

                    line_info = str(light['type']) + ' ' + power_str + \
                                ' ' + color_str  + ' ' + pos_corner_str + \
                                ' ' + v1_str + ' ' +  v2_str
                    # print line_info

                elif light['type'] == 'LineLight': #LineLights are modelled as SpotLights
                    pos1 = light_pos_from_trans(node['transform'],light['position'])
                    pos2 = light_pos_from_trans(node['transform'],light['position2'])
                    v1 = pos2 - pos1
                    v2_unscaled = np.array([-v1[2]/v1[0], 0., 1.])
                    v2 = (lineLight_width/np.linalg.norm(v2_unscaled)) * v2_unscaled 
                    if (np.cross(v1,v2)[1] > 0): #if light dir facing up
                        v2 = -v2 #flip v2 to make light dir face down

                    pos_corner = pos1 - 0.5*v2

                    pos_corner_str = ' '.join(str(i) for i in pos_corner)
                    v1_str = ' '.join(str(i) for i in v1)
                    v2_str = ' '.join(str(i) for i in v2)

                    print 'LINELIGHT', pos1, pos2, v1, v2, pos_corner

                    line_info = str(light['type']) + ' ' + power_str + \
                                ' ' + color_str  + ' ' + pos_corner_str + \
                                ' ' + v1_str + ' ' +  v2_str  
                    # print line_info

                lights_info.append(line_info)
                print >> log, node['id'].split('_')[1], line_info
                light_index_list.append(light_index)
                light_index += 1;

            for r in range(room_count):
                node_indices = rooms_node_indices[r]
                node_id = int(node['id'].split('_')[1])
                if node_id in node_indices:
                    rooms_with_light.append((r+1)) 
                    lights_in_rooms_byNodeID[r].append(node_id)
                    [lights_in_rooms_byIndex[r].append(i) for i in light_index_list]
                    light_index_list = []

print 'Total num of lights:',len(lights_info)
rooms_with_light = sorted(set(rooms_with_light)) #room index starts 1
print 'Rooms with lights:', list(rooms_with_light)
print >> log, "Rooms with lights (starts from 1):",list(rooms_with_light)
print >> log, "Lights location by NodeID"
print >> log, lights_in_rooms_byNodeID
print >> log, "Lights location by Index (starts from 0)"
print >> log, lights_in_rooms_byIndex
## Format for lights_info:
# PointLight power rgb pos(xyz) radius
# SpotLight/LineLight  power rgb pos(xyz) v1 v2
toSave = [lights_info, rooms_with_light, lights_in_rooms_byIndex]
f = open(house_temp_dir + houseID + '_lighting.pckl','wb')
pickle.dump(toSave, f)
f.close()

print 'Lighting info saved.'
