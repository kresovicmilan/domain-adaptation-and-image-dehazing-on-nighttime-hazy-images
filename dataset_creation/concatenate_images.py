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

def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def concatenate(hazy_path, gt_path, dest_path):
    im1 = Image.open(hazy_path)
    im2 = Image.open(gt_path)
    concat_img = get_concat_h(im1, im2)
    concat_img.save(dest_path)

if __name__ == '__main__':
    src_hazy_dir = ""
    src_gt_dir = "C"
    dst_concat_dir = ""
    image_names = get_img_names(src_gt_dir)

    for img_name in image_names:
        concatenate(src_hazy_dir + '\\' + img_name, src_gt_dir + '\\' + img_name, dst_concat_dir + '\\' + img_name)