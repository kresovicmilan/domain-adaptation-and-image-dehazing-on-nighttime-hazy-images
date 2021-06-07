import os
import os.path
import random
import shutil

seed = 42
random.seed(seed)

IMG_EXTENSIONS = [
    '.jpg', '.JPG', '.jpeg', '.JPEG',
    '.png', '.PNG', '.ppm', '.PPM', '.bmp', '.BMP',
]

### Combined dataset
"""DATASETS_HAZY = ['3R\\nighttimeHazy', 'NightHaze\\NightHaze-1', 'NightHaze\\NightHaze-2']
DATASETS_GT = ['3R\\nighttimeHazy', 'NightHaze\\Haze-Free', 'NightHaze\\Haze-Free']
DATASETS_CLEAR = ['3R\\clear_images', 'NightHaze\\Haze-Free', 'NightHaze\\Haze-Free']
PREFIX = ['3r', 'nh1', 'nh2']
DST_HAZY = 'Prep\\synt\\imgs'
DST_GT = 'Prep\\synt\\gt'
DST_CLEAR_DEPTH = 'Prep\\synt\\clear_depth'
NUM_PER_DS = 2400"""

### NightHaze dataset
"""DATASETS_HAZY = ['NightHaze\\NightHaze-1', 'NightHaze\\NightHaze-2']
DATASETS_GT = ['NightHaze\\Haze-Free', 'NightHaze\\Haze-Free']
DATASETS_CLEAR = ['NightHaze\\Haze-Free', 'NightHaze\\Haze-Free']
PREFIX = ['nh1', 'nh2']
DST_HAZY = 'PrepNH\\synt\\imgs'
DST_GT = 'PrepNH\\synt\\gt'
DST_CLEAR_DEPTH = 'PrepNH\\synt\\clear_depth'
NUM_PER_DS = 3500"""

### 3R dataset
DATASETS_HAZY = ['3R\\nighttimeHazy']
DATASETS_GT = ['3R\\nighttimeHazy']
DATASETS_CLEAR = ['3R\\clear_images']
PREFIX = ['3r']
DST_HAZY = 'Prep3R\\synt\\imgs'
DST_GT = 'Prep3R\\synt\\gt'
DST_CLEAR_DEPTH = 'Prep3R\\synt\\clear_depth'
NUM_PER_DS = 7000

def is_image_file(filename):
    return any(filename.endswith(extension) for extension in IMG_EXTENSIONS)

def copy_hazy(dir, selected_ds):
    for idx, ds in enumerate(selected_ds):
        prefix = PREFIX[idx]
        for path in ds:
            part_1 = path.split("\\")[-1]
            final = dir + DST_HAZY + "\\" + prefix + "_" + part_1
            shutil.copy(path, final)

def copy_gt(dir, gt_ds):
    for idx, ds in enumerate(gt_ds):
        prefix = PREFIX[idx]
        for path in ds:
            if prefix == '3r':
                part_1 = path.split("\\")[-1].split("_")[0]
                ext = path.split("\\")[-1].split(".")[-1]
                ending = part_1 + "_NighttimeHazy_1." + ext
            else:
                part_2 = path.split("\\")[-1]
                ending = 'hazy' + part_2
            final = dir + DST_GT + "\\" + prefix + "_" + ending
            shutil.copy(path, final)

def copy_dept(dir, depth_ds):
    for idx, ds in enumerate(depth_ds):
        prefix = PREFIX[idx]
        for path in ds:
            part_1 = path.split("\\")[-1]
            if prefix == '3r':
                part_1 = path.split("\\")[-1].split(".")[0]
                ext = path.split("\\")[-1].split(".")[-1]
                ending = part_1 + '_NighttimeHazy_1.' + ext 
            else:
                part_1 = path.split("\\")[-1]
                ending = 'hazy' + part_1
            final = dir + DST_CLEAR_DEPTH + "\\" + prefix + "_" + ending
            shutil.copy(path, final)

if __name__ == '__main__':
    dir = '..\\'
    images_ds = []
    assert os.path.isdir(dir), '%s is not a valid directory' % dir

    for ds in DATASETS_HAZY:
        images = []
        for root, _, fnames in sorted(os.walk(dir + ds)):
            for fname in fnames:
                if is_image_file(fname):
                    if not 'lowLight' in fname.split("\\")[-1]:
                        path = os.path.join(root, fname)
                        images.append(path)
        images_ds.append(images)
    
    selected_ds = []
    for ds in images_ds:
        selected_ds.append(random.sample(ds, NUM_PER_DS))
    
    gt_ds = []
    for idx, ds in enumerate(selected_ds):
        gt = []
        base = DATASETS_GT[idx]
        if base == '3R\\nighttimeHazy':
            for path in ds:
                part_1 = dir + base
                part_2 = path.split('\\')[-1].split("_")[0]
                ext = path.split('\\')[-1].split(".")[-1]
                final = part_1 + "\\" + part_2 + "_lowLight_1." + ext
                gt.append(final)
        else:
            for path in ds:
                part_1 = dir + base
                part_2 = path.split("\\")[-1].split('hazy')[-1]
                final = part_1 + "\\" + part_2
                gt.append(final)
        gt_ds.append(gt)
    
    depth_ds = []
    for idx, ds in enumerate(gt_ds):
        depth = []
        base = DATASETS_CLEAR[idx]
        if base == '3R\\clear_images':
            for path in ds:
                part_1 = dir + base
                part_2 = path.split("\\")[-1].split("_")[0]
                ext = path.split("\\")[-1].split(".")[-1]
                final = part_1 + "\\" + part_2 + "." + ext
                depth.append(final)
        else:
            for path in ds:
                depth.append(path)
        depth_ds.append(depth)

    #copy_hazy(dir, selected_ds)
    #copy_gt(dir, gt_ds)
    #copy_dept(dir, depth_ds)

    #print(gt_ds[1][-10:])


    #print(selected_ds[0][-50:])