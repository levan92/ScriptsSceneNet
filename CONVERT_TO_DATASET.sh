#!/bin/bash

# User Parameters
#houseID=ffe9e14822570206cce1fc7259adda71
houseID=0004dd3cb11e50530676f77b55262d38
#houseID=a55f64ca8fdee38a554429d7f7ac8b50
#houseID=fff3ca3254c364df22f15646ad160400
output_directory=/scratch/el216/output_scenenet
dataset_directory=/scratch/el216/scenenet_dataset
SET=train
#SET=val

echo 'parsing house '$houseID' into dataset format and copying to '$dataset_directory/$SET'.' 

cd $output_directory/$houseID

echo 'processing rgb..'
cd photo
for i in *.jpg
do
    basename=${i%.jpg}
    cp $i $dataset_directory/$SET/$houseID"_"$basename"_rgb.jpg"    
done

echo 'processing labels..'
cd ../labels
for i in *.png
do
    basename=${i%.png}
    cp $i $dataset_directory/$SET/$houseID"_"$basename"_label.png"    
done

echo 'processing depth..'
cd ../depth
for i in *.png
do
    basename=${i%.png}
    cp $i $dataset_directory/$SET/$houseID"_"$basename"_depth.png"    
done

echo 'Copied to '$dataset_directory/$SET'.'

size=$(ls -1 $dataset_directory/$SET | wc -l)
echo "$SET set current size: $((size/3))"


