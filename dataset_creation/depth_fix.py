import os
import random
import shutil

seed = 42
random.seed(seed)

IMG_EXTENSIONS = [
    '.jpg', '.JPG', '.jpeg', '.JPEG',
    '.png', '.PNG', '.ppm', '.PPM', '.bmp', '.BMP',
]

def is_image_file(filename):
    return any(filename.endswith(extension) for extension in IMG_EXTENSIONS)

def get_img_paths(src_concat_dir):
    images_path = []
    for root, _, fnames in sorted(os.walk(src_concat_dir)):
        for fname in fnames:
            if is_image_file(fname):
                path = os.path.join(root, fname)
                images_path.append(path)
    return images_path

if __name__ == '__main__':
    src_test_dir = ""
    src_depth_dir = ""
    dst_test_depth_dir = ""

    image_paths = get_img_paths(src_test_dir)

    for path in image_paths:
        img_name = path.split("\\")[-1]
        shutil.copy(src_depth_dir + "\\" + img_name, dst_test_depth_dir + "\\" + img_name)