import os
import shutil
output_dir = "/scratch/el216/output_scenenet/"
dataset_dir = "/scratch/el216/scenenet_dataset/"

sets = next(os.walk(dataset_dir))[1]

for set_ in sets:
    set_path = os.path.join(dataset_dir, set_)
    files = next(os.walk(set_path))[2]
    for file in files:
        if file.endswith("_label.png"):
            dataset_label_path = os.path.join(set_path, file)
            [houseID, room, frame, _] = file.split("_")
            house_path = os.path.join(output_dir, houseID)
            room_path = os.path.join(house_path, houseID + "_" + room)
            labels_dir_path = os.path.join(room_path, "labels")
            updated_label_path = os.path.join(labels_dir_path,frame+".png")
            shutil.copy(updated_label_path, dataset_label_path)
            # print os.path.exists(updated_label_path), os.path.exists(dataset_label_path)
            # print updated_label_path,"copied to",dataset_label_path
