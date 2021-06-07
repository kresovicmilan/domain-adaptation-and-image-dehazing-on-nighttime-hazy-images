from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import random
from random import randrange
import os

seed = 42

random.seed(seed)

IMG_EXTENSIONS = [
    '.jpg', '.JPG', '.jpeg', '.JPEG',
    '.png', '.PNG', '.ppm', '.PPM', '.bmp', '.BMP',
]

def is_image_file(filename):
    return any(filename.endswith(extension) for extension in IMG_EXTENSIONS)

def get_img_names(src_gt_dir):
    image_names = []
    for root, _, fnames in sorted(os.walk(src_gt_dir)):
        for fname in fnames:
            if is_image_file(fname):
                image_names.append(fname)
    return image_names

def disparity_normalization(disp): # disp is an array in uint8 data type
        # disp_norm = cv2.normalize(src=disp, dst= disp, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX)
        _min = np.amin(disp)
        _max = np.amax(disp)
        #disp_norm = disp - _min * 255.0 / (_max - _min)
        disp_norm = (disp - _min) * 255.0 / (_max - _min)
        disp_norm = np.uint8(disp_norm)

        return disp_norm 

def apply_normalization(src_depth_dir, image_names):
    for img_name in image_names:
        img_path = src_depth_dir + "\\" + img_name
        img = Image.open(img_path)
        norm_img = disparity_normalization(img)
        img = Image.fromarray(norm_img)
        img.save(img_path)

if __name__ == '__main__':
    src_depth_dir = ""
    image_names = get_img_names(src_depth_dir)

    apply_normalization(src_depth_dir, image_names)