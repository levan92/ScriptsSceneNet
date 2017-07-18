import sys
import imgaug as ia
from imgaug import augmenters as iaa
import pathlib
import cv2
import numpy as np
import os

def get_item_paths(path):
    items = []
    for p in pathlib.Path(path).iterdir():
        # if str(p).endswith('_rgb.jpg') and 'aug_rgb' not in str(p):
        if str(p).endswith('_rgb.jpg'):
            depth_path = str(p).replace('_rgb.jpg','_depth.png')
            if not os.path.exists(depth_path): 
                print depth_path,'does not exist.'
                depth_path = ''
            label_path = str(p).replace('_rgb.jpg','_label.png')
            if not os.path.exists(label_path): 
                print label_path,'does not exist.'
                label_path = ''
            items.append({'image':str(p), 
                          'depth':depth_path, 
                          'label':label_path })
    return items

def read_item(input_item):
    image = cv2.imread(input_item['image']).astype(np.float32)
    image = cv2.resize(image,(320,240),interpolation=cv2.INTER_LINEAR)
    depth = []
    if input_item['depth']:
        # depth = cv2.imread(input_item['depth'],-1|cv2.IMREAD_ANYDEPTH).astype(np.float32)
        depth = cv2.imread(input_item['depth'],-1|cv2.IMREAD_ANYDEPTH).astype(np.uint16)
        depth = cv2.resize(depth,(320,240),interpolation=cv2.INTER_LINEAR)
    label = []
    if input_item['label']:
        label = cv2.imread(input_item['label'],-1|cv2.IMREAD_ANYDEPTH).astype(np.uint8)
        label = cv2.resize(label,(320,240),interpolation=cv2.INTER_NEAREST)
    # Rotate axis to produce correct image size (i.e. CHW not HWC)
    # image = np.rollaxis(image,2)
    # depth = np.expand_dims(depth,axis=0)
    # label = np.expand_dims(label,axis=0)
    # HWC settings for data aug:
    depth = np.expand_dims(depth,axis=2)
    label = np.expand_dims(label,axis=2)
    # Note extra dict items not in the example placeholder are passed
    # into inference etc as a list
    return {'image':image,'depth':depth,'label':label,'filename':os.path.split(input_item['label'])[1]}

def resize_linear(images):
    newImages = []
    for image in images:
        newImages.append(cv2.resize(image,(320,240),interpolation=cv2.INTER_LINEAR))
    return newImages

def resize_nearest(labels):
    newLabels = []
    for label in labels:
        newLabels.append(cv2.resize(label,(320,240),interpolation=cv2.INTER_NEAREST))
    return newLabels

def save_images(images, type, items, root_dir):
    for i, image in enumerate(images):
        img_name = items[i]['filename']
        rep = 1
        if 'aug' in img_name:
            first, second = img_name.split("aug",1)
            rep = int(second[0])
            img_name = first + "aug" + str(rep) + "_" + type + '.png'
        else:
            img_name = img_name.replace('_label.','_aug'+str(rep)+'_'+type+'.')
        if type == "rgb":
            img_name = img_name.replace('.png','.jpg')
        save_path = os.path.join(root_dir, img_name)
        while os.path.exists(save_path):
            rep += 1
            save_path = save_path.replace('_aug'+str(rep-1),'_aug'+str(rep))
        cv2.imwrite(save_path,image)
        print save_path,'saved.'

def main(dataset_dir, augmenters):
    flip = zoom = blur = noise = contrast = brightness = False
    for aug in augmenters: 
        if aug == "flip": 
            flip = True
            print "Flip augmenter activated"
        elif aug == "zoom": 
            zoom = True
            print "Zoom augmenter activated"
        elif aug == "blur": 
            blur = True
            print "Blur augmenter activated"
        elif aug == "noise": 
            noise = True
            print "Noise augmenter activated"
        elif aug == "contrast": 
            contrast = True
            print "Contrast augmenter activated"
        elif aug == "brightness": 
            brightness = True
            print "Brightness augmenter activated"
        else: 
            print "Warning: Argument not recognised."

    if not any([flip,zoom,blur,noise,contrast,brightness]):
        print "No augmenter chosen, exiting.."
        sys.exit()

    seq = iaa.Sequential([iaa.Noop()])  #initialiser, Noop does nothing
    if flip: # horizontal flip
        seq.add( iaa.Fliplr(1.0, name="Flip") ) 
    if zoom: # crop images from each side by 0 to 16px (randomly chosen)
        seq.add( iaa.Crop(px=(0, 16), keep_size=False, name="Zoom") )
    if blur: # blur images, sigma of 0 to 2.5
        seq.add( iaa.GaussianBlur(sigma=(0., 2.0), name="Blur") )
    if noise:
        seq.add( iaa.AdditiveGaussianNoise(scale=(0.0*255, 0.05*255), name="Noise") )
    if contrast:
        seq.add( iaa.ContrastNormalization((0.5, 2.0), name="Contrast") )
    if brightness:
        seq.add( iaa.Multiply((0.25, 2.0), name="Brightness") )

    def activator_labels(images, augmenter, parents, default):
        if augmenter.name in ["Blur","Noise","Contrast","Brightness"]:
            return False
        else:
            return default
    hooks_labels = ia.HooksImages(activator=activator_labels)
    seq_det = seq.to_deterministic()
    
    print "Getting image paths..."
    item_paths = get_item_paths(dataset_dir)  
    items=[]  
    print "Reading images..."
    for path in item_paths:
        items.append(read_item(path))
    images = [item['image'] for item in items if 'image' in item]
    labels = [item['label'] for item in items if 'label' in item]
    depths = [item['depth'] for item in items if 'depth' in item]
    # print np.shape(images)
    # print np.shape(labels)

    print "Images read, augmenting images now..."
    images_aug = seq_det.augment_images(images)
    images_aug = resize_linear(images_aug)
    print 'Augmenting labels...'
    labels_aug = seq_det.augment_images(labels, hooks=hooks_labels)
    labels_aug = resize_nearest(labels_aug)
    print 'Augmenting depth maps...'
    depths_aug = seq_det.augment_images(depths, hooks=hooks_labels)
    depths_aug = resize_linear(depths_aug)
    print "Augmentation done, saving augmented images..."
    save_images(images_aug, "rgb", items, dataset_dir)
    save_images(labels_aug, "label", items, dataset_dir)
    save_images(depths_aug, "depth", items, dataset_dir)
    print "Done."

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
