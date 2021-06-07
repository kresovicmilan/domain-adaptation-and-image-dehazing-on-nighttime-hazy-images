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

def get_img_names(src_test_dir):
    image_names = []
    for root, _, fnames in sorted(os.walk(src_test_dir)):
        for fname in fnames:
            if is_image_file(fname):
                image_names.append(fname)
    return image_names

if __name__ == '__main__':
    src_test_dir = ""
    dst_haze_dir = ""

    image_names = get_img_names(src_test_dir)
    for img_name in image_names:
        img = Image.open(src_test_dir + "\\" + img_name)
        width, height = img.size
        width_cutoff = width // 2
        box = (0, 0, width_cutoff, height)
        hazy = img.crop(box)
        hazy.save(dst_haze_dir + "\\" + img_name)
