import os
import numpy
import cv2
import torch
import matplotlib.pyplot as plt

IMG_EXTENSIONS = [
    '.jpg', '.JPG', '.jpeg', '.JPEG',
    '.png', '.PNG', '.ppm', '.PPM', '.bmp', '.BMP',
]

def is_image_file(filename):
    return any(filename.endswith(extension) for extension in IMG_EXTENSIONS)

def get_img_paths(src_clear_dept_dir):
    images_path = []
    for root, _, fnames in sorted(os.walk(src_clear_dept_dir)):
        for fname in fnames:
            if is_image_file(fname):
                path = os.path.join(root, fname)
                images_path.append(path)
    return images_path

if __name__ == '__main__':
    model_type = "DPT_Large"     # MiDaS v3 - Large     (highest accuracy, slowest inference speed)
    #model_type = "DPT_Hybrid"   # MiDaS v3 - Hybrid    (medium accuracy, medium inference speed)
    #model_type = "MiDaS_small"  # MiDaS v2.1 - Small   (lowest accuracy, highest inference speed)

    midas = torch.hub.load("intel-isl/MiDaS", model_type)
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    midas.to(device)
    midas.eval()

    midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")

    if model_type == "DPT_Large" or model_type == "DPT_Hybrid":
        transform = midas_transforms.dpt_transform
    else:
        transform = midas_transforms.small_transform

    ### Uncomment for depth estimation of synt images
    src_clear_depth_dir = ""
    dst_depth_dir = ""
    image_paths = get_img_paths(src_clear_depth_dir)

    ### Uncomment for depth estimation of train real images
    """src_real_dir = ""
    dst_depth_dir = ""
    image_paths = get_img_paths(src_real_dir)"""

    ### Uncomment for depth estimation of val real images
    """src_real_val_dir = ""
    dst_depth_dir = ""
    image_paths = get_img_paths(src_real_val_dir)"""

    for img_path in image_paths:
        img_name = img_path.split("\\")[-1]
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        input_batch = transform(img).to(device)

        with torch.no_grad():
            prediction = midas(input_batch)

            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=img.shape[:2],
                mode="bicubic",
                align_corners=False,
            ).squeeze()

        output = prediction.cpu().numpy()
        dst_img_path = dst_depth_dir + "\\" + img_name
        plt.imsave(dst_img_path, output, cmap='gray')