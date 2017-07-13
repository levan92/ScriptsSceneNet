import instance2classFromInfoLog_scratch_outputs as labelling
import os

output_dir = "/scratch/el216/output_scenenet"

# for each house
houses = next(os.walk(output_dir))[1]
for house in houses:
    labelling.main(house)