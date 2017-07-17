import sys
from imgaug import augmenters as iaa
import pathlib
import cv2
import numpy as np
import os

def get_item_paths(path):
    items = []
    for p in pathlib.Path(path).iterdir():
        if str(p).endswith('_rgb.jpg'):
            items.append({'image':str(p), 
                'depth':str(p).replace('_rgb.jpg','_depth.png'), 
                'label':str(p).replace('_rgb.jpg','_label.png')})
    return items

def read_item(input_item):
    image = cv2.imread(input_item['image']).astype(np.float32)
    # image = cv2.resize(image,(320,240),interpolation=cv2.INTER_LINEAR)
    depth = cv2.imread(input_item['depth'],-1|cv2.IMREAD_ANYDEPTH).astype(np.float32)
    # depth = cv2.resize(depth,(320,240),interpolation=cv2.INTER_LINEAR)
    label = cv2.imread(input_item['label'],-1|cv2.IMREAD_ANYDEPTH).astype(np.uint8)
    # label = cv2.resize(label,(320,240),interpolation=cv2.INTER_NEAREST)
    # Rotate axis to produce correct image size (i.e. CHW not HWC)
    # image = np.rollaxis(image,2)
    # depth = np.expand_dims(depth,axis=0)
    # label = np.expand_dims(label,axis=0)
    # HWC settings for data aug:
    depth = np.expand_dims(depth,axis=1)
    label = np.expand_dims(label,axis=1)
    # Note extra dict items not in the example placeholder are passed
    # into inference etc as a list
    return {'image':image,'depth':depth,'label':label,'filename':os.path.split(input_item['label'])[1]}

def save_images(prefix,input_images,input_depths,input_labels,arg_max_preds):
    # Save labels images depths and predictions
    num_to_save = input_images.shape[0]
    for id_to_save in range(num_to_save):
        image = np.rollaxis(input_images[id_to_save],2)
        image = np.rollaxis(image,2).astype(np.uint8)
        cv2.imwrite('./training_image_saves/{0}_{1}_image.png'.format(prefix,id_to_save),image)
        cv2.imwrite('./training_image_saves/{0}_{1}_depth.png'.format(prefix,id_to_save),np.uint16(np.squeeze(input_depths[id_to_save])))
        label_img = np.zeros((240,320,3))
        for colour_index in range(3):
            label_img[:,:,colour_index] = self.numpy_lookup[colour_index][np.int32(input_labels[id_to_save])]
        cv2.imwrite('./training_image_saves/{0}_{1}_label.png'.format(prefix,id_to_save),label_img)
        prediction_img = np.zeros((240,320,3))
        for colour_index in range(3):
            if len(arg_max_preds.shape) == 2:
                assert num_to_save == 1
                prediction_img[:,:,colour_index] = self.numpy_lookup[colour_index][np.int32(arg_max_preds)]
            else:
                prediction_img[:,:,colour_index] = self.numpy_lookup[colour_index][np.int32(arg_max_preds[id_to_save])]
        cv2.imwrite('./training_image_saves/{0}_{1}_predictions.png'.format(prefix,id_to_save),prediction_img)
    return True

def main(dataset_dir):
    seq = iaa.Sequential([
        iaa.Crop(px=(0, 30)), # crop images from each side by 0 to 16px (randomly chosen)
        iaa.Fliplr(1.0), # horizontally flip 50% of the images
        iaa.GaussianBlur(sigma=(0, 3.0)), # blur images, sigma of 0 to 3.0
        iaa.AdditiveGaussianNoise(scale=(0.0*255, 0.05*255))
    ])
    item_paths = get_item_paths(dataset_dir)  
    items=[]  
    for path in item_paths:
        items.append(read_item(path))
    images = [item['image'] for item in items if 'image' in item]
    images_aug = seq.augment_images(images)

    for i, image in enumerate(images_aug):
        img_name = os.path.splitext(items[i]['filename'])[0].replace('label','rgbaug')
        save_path = dataset_dir + img_name + '.jpg'
        cv2.imwrite(save_path,image)
        print save_path,'saved.'
    # for batch_idx in range(1000):
    #     # 'images' should be either a 4D numpy array of shape (N, height, width, channels)
    #     # or a list of 3D numpy arrays, each having shape (height, width, channels).
    #     # Grayscale images must have shape (height, width, 1) each.
    #     # All images must have numpy's dtype uint8. Values are expected to be in
    #     # range 0-255.
    #     images = load_batch(batch_idx)
    #     images_aug = seq.augment_images(images)
    #     train_on_images(images_aug)

if __name__ == '__main__':
    main(sys.argv[1])
