import sys
import os
import pathlib
import itertools
import numpy as np
from shutil import copy2

def main(set_base_path, set_path, req_size):
    if not os.path.exists(set_path):
        os.mkdir(set_path)
    rooms = []
    images_in_rooms = []
    total_num = 0
    for image_path in pathlib.Path(set_base_path).iterdir():
        total_num += 1
        image_name = os.path.basename(str(image_path))
        split_info = image_name.split('_')
        room_name = "_".join(split_info[:2])
        frame_name = "_".join(split_info[:3])
        try:
            r_index = rooms.index(room_name)
        except ValueError:
            r_index = -1

        if r_index == -1:
            rooms.append(room_name)
            images_in_rooms.append([frame_name])
        else:
            images_in_room = images_in_rooms[r_index] #shallow copy
            if frame_name not in images_in_room:
                images_in_room.append(frame_name)
    n = 0
    sampled_images = []
    for r in itertools.cycle(range(len(rooms))):
        images_in_room = images_in_rooms[r]
        if not images_in_room:
            continue
        chosen = np.random.choice(images_in_room)
        images_in_room.remove(chosen)
        sampled_images.append(chosen)
        n += 1
        if n >= req_size:
            break

    for sample in sampled_images:
        sample_rgb = sample + "_rgb.jpg"
        sample_depth = sample + "_depth.png"
        sample_label = sample + "_label.png"
        sample_rgb_path = os.path.join(set_base_path, sample_rgb)
        sample_depth_path = os.path.join(set_base_path, sample_depth)
        sample_label_path = os.path.join(set_base_path, sample_label)
        copy2(sample_rgb_path, set_path)
        copy2(sample_depth_path, set_path)
        copy2(sample_label_path, set_path)
        print "Copied set of",sample,'images to',set_path

    print "Num frame sets in set now:", len([name for name in os.listdir(set_path)])/3.0


if __name__ == "__main__":
    main(os.path.normpath(sys.argv[1]), os.path.normpath(sys.argv[2]), int(sys.argv[3]))