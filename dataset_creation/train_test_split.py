import os
import random
import shutil

seed = 42
random.seed(seed)

NUM_TRAIN_IMG = 6000
NUM_TEST_IMG = 1200

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

def train(concat_paths, depth_paths, dst_train_dir, dst_train_depth_dir):
    for idx, path in enumerate(concat_paths[:NUM_TRAIN_IMG]):
        img_name = path.split("\\")[-1]
        shutil.copy(path, dst_train_dir + "\\" + img_name)
        shutil.copy(depth_paths[idx], dst_train_depth_dir + "\\" + img_name)

def test(concat_paths, depth_paths, dst_test_dir, dst_test_depth_dir):
    for idx, path in enumerate(concat_paths[NUM_TRAIN_IMG:]):
        img_name = path.split("\\")[-1]
        shutil.copy(path, dst_test_dir + "\\" + img_name)
        shutil.copy(depth_paths[NUM_TRAIN_IMG + idx], dst_test_depth_dir + "\\" + img_name)

if __name__ == '__main__':
    src_concat_dir = ""
    src_depth_dir = ""
    dst_train_dir = ""
    dst_train_depth_dir = ""
    dst_test_dir = ""
    dst_test_depth_dir = ""

    concat_paths = get_img_paths(src_concat_dir)
    random.shuffle(concat_paths)

    depth_paths = []
    for concat in concat_paths:
        img_name = concat.split("\\")[-1]
        depth_path = src_depth_dir + "\\" + img_name
        depth_paths.append(depth_path)
    
    train(concat_paths, depth_paths, dst_train_dir, dst_train_depth_dir)
    test(concat_paths, depth_paths, dst_test_dir, dst_test_depth_dir)

    #print(concat_paths[2:4])


