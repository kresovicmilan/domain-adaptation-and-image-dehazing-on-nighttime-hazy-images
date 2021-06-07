from PIL import Image
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

if __name__ == '__main__':
    src_imgs_dir = ""
    src_gt_dir = ""
    src_depth_dir = ""
    image_names = get_img_names(src_gt_dir)

    dx_nh2 = 63
    dy_nh2 = 63
    for img_name in image_names:
        if img_name.split("_")[0] == "nh2":
            imgs_path = src_imgs_dir + "\\" + img_name
            gt_path = src_gt_dir + "\\" + img_name
            depth_path = src_depth_dir + "\\" + img_name

            imgs = Image.open(imgs_path)
            gt = Image.open(gt_path)
            depth = Image.open(depth_path)

            box_imgs = (dx_nh2, dy_nh2, imgs.size[0], imgs.size[1])
            box_gt = (0, 0, gt.size[0]-dx_nh2, gt.size[1]-dy_nh2)
            box_depth = (0, 0, depth.size[0]-dx_nh2, depth.size[1]-dy_nh2)

            imgs = imgs.crop(box_imgs)
            imgs.save(imgs_path)

            gt = gt.crop(box_gt)
            gt.save(gt_path)

            depth = depth.crop(box_depth)
            depth.save(depth_path)