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

def resize_and_crop(img_path, modified_path, size, crop_type='random', decided_box = []):
    """
    Resize and crop an image to fit the specified size.

    args:
    img_path: path for the image to resize.
    modified_path: path to store the modified image.
    size: `(width, height)` tuple.
    crop_type: can be 'top', 'middle' or 'bottom', depending on this
    value, the image will cropped getting the 'top/left', 'middle' or
    'bottom/right' of the image to fit the size.
    raises:
    Exception: if can not open the file in img_path of there is problems
    to save the image.
    ValueError: if an invalid `crop_type` is provided.
    """
    # If height is higher we resize vertically, if not we resize horizontally
    img = Image.open(img_path)
    # Get current and desired ratio for the images
    img_ratio = img.size[0] / float(img.size[1])
    ratio = size[0] / float(size[1])
    box = []
    #The image is scaled/cropped vertically or horizontally depending on the ratio
    if ratio > img_ratio:
        img = img.resize((size[0], int(round(size[0] * img.size[1] / img.size[0]))),
            Image.ANTIALIAS)
        # Crop in the top, middle or bottom
        if crop_type == 'top':
            box = (0, 0, img.size[0], size[1])
        elif crop_type == 'middle':
            box = (0, int(round((img.size[1] - size[1]) / 2)), img.size[0],
                int(round((img.size[1] + size[1]) / 2)))
        elif crop_type == 'bottom':
            box = (0, img.size[1] - size[1], img.size[0], img.size[1])
        elif crop_type == 'random':
            leftover_x1 = img.size[0] - size[0]
            leftover_y1 = img.size[1] - size[1]
            if leftover_x1 == 0:
                x1 = 0
            else:
                x1 = randrange(0, leftover_x1)
            if leftover_y1 == 0:
                y1 = 0
            else:
                y1 = randrange(0, leftover_y1)
            box = (x1, y1, x1 + size[0], y1 + size[1])
        elif crop_type == 'decided':
            box = decided_box
        else :
            raise ValueError('ERROR: invalid value for crop_type')
        img = img.crop(box)
    elif ratio < img_ratio:
        img = img.resize((int(round(size[1] * img.size[0] / img.size[1])), size[1]),
            Image.ANTIALIAS)
        # Crop in the top, middle or bottom
        if crop_type == 'top':
            box = (0, 0, size[0], img.size[1])
        elif crop_type == 'middle':
            box = (int(round((img.size[0] - size[0]) / 2)), 0,
                int(round((img.size[0] + size[0]) / 2)), img.size[1])
        elif crop_type == 'bottom':
            box = (img.size[0] - size[0], 0, img.size[0], img.size[1])
        elif crop_type == 'random':
            leftover_x1 = img.size[0] - size[0]
            leftover_y1 = img.size[1] - size[1]
            if leftover_x1 == 0:
                x1 = 0
            else:
                x1 = randrange(0, leftover_x1)
            if leftover_y1 == 0:
                y1 = 0
            else:
                y1 = randrange(0, leftover_y1)
            box = (x1, y1, x1 + size[0], y1 + size[1])
        elif crop_type == 'decided':
            box = decided_box
        else :
            raise ValueError('ERROR: invalid value for crop_type')
        img = img.crop(box)
    else :
        img = img.resize((size[0], size[1]),
            Image.ANTIALIAS)
    # If the scale is the same, we do not need to crop
    img.save(modified_path)
    return box

if __name__ == '__main__':
    src_gt_dir = ""
    dst_gt_dir = ""
    src_hazy_dir = ""
    dst_hazy_dir = ""
    #src_clear_depth_dir = ""
    #dst_clear_depth_dir = ""
    src_depth_dir = ""
    dst_depth_dir = ""

    """src_real_dir = ""
    dst_real_dir = ""
    src_real_val_dir = ""
    dst_real_val_dir = ""

    src_real_depth_dir = ""
    dst_real_depth_dir = ""
    src_real_depth_val_dir = ""
    dst_real_depth_val_dir = "" """
    
    ### Uncomment to prepare synt images
    image_names = get_img_names(src_gt_dir)

    for img_name in image_names:
        box = resize_and_crop(src_gt_dir + "\\" + img_name, dst_gt_dir + "\\" + img_name, [400, 400])
        resize_and_crop(src_hazy_dir + "\\" + img_name, dst_hazy_dir + "\\" + img_name, [400, 400], crop_type='decided', decided_box=box)
        resize_and_crop(src_depth_dir + "\\" + img_name, dst_depth_dir + "\\" + img_name, [400, 400], crop_type='decided', decided_box=box)


    ### Uncomment to prepare real images
    """image_names = get_img_names(src_real_dir)
    image_val_names = get_img_names(src_real_val_dir)

    for img_name in image_names:
        box = resize_and_crop(src_real_dir + "\\" + img_name, dst_real_dir + "\\" + img_name, [400, 400])
        resize_and_crop(src_real_depth_dir + "\\" + img_name, dst_real_depth_dir + "\\" + img_name, [400, 400], crop_type='decided', decided_box=box)
    
    for img_name in image_val_names:
        box = resize_and_crop(src_real_val_dir + "\\" + img_name, dst_real_val_dir + "\\" + img_name, [400, 400])
        resize_and_crop(src_real_depth_val_dir + "\\" + img_name, dst_real_depth_val_dir + "\\" + img_name, [400, 400], crop_type='decided', decided_box=box)"""