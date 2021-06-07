# Domain-adaptation-and-image-dehazing-on-nighttime-hazy-images
Coursework project: Advanced Image Processing and Deep learning - [UJM](https://www.univ-st-etienne.fr/fr/index.html), France

- Project owners: [Milan Kresovic](https://github.com/kresovicmilan), [David Díaz Estrada](https://github.com/DavidDZ7), [Thong Nguyen](https://github.com/ThongNguyen551).
- This project is inspired from this [paper](https://openaccess.thecvf.com/content_CVPR_2020/papers/Shao_Domain_Adaptation_for_Image_Dehazing_CVPR_2020_paper.pdf) and this [project](https://github.com/HUSTSYJ/DA_dahazing) to implement a domain adaptation framework for nighttime image dehazing.

## Evironment and Packages
1. Python 3.7
2. Pytorch 1.8.1
3. CUDA 11.1
4. Ubunti 18.04
5. Visdom
6. Dominate

To install the packages:
```
pip3 install torch==1.8.1+cu111 torchvision==0.9.1+cu111 torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html visdom dominate
```
## Dataset 

We created our own real-world images and combine with the synthetic images [Night Haze](https://pan.baidu.com/s/1cY8O5H8EYIwetPdb6xdupA#list/path=%2F) for training and test: [Download](https://drive.google.com/drive/folders/1nuTm4oStHOdNhtiDDbiU8M_hcKkSLA_9?usp=sharing) 

## Workflow
### Training

1. Train CycleGAN - translation network
```
python train.py --dataroot ./datasets/dehazing --name run_cyclegan --learn_residual --resize_or_crop crop --display_freq 100 --print_freq 100 --display_port 8091 --which_model_netG resnet_9blocks --lambda_A 1 --lambda_B 1 --lambda_identity 0.1   --niter 90 --niter_decay 0 --fineSize 256 --no_html --batchSize 2  --gpu_id 2 --update_ratio 1 --unlabel_decay 0.99 --save_epoch_freq 1 --model cyclegan
```

2. Train Fr using the pretrained CycleGAN
```
python train.py  --dataroot ./datasets/dehazing --name run_fr_depth --lambda_Dehazing 10 --lambda_Dehazing_DC 1e-2 --lambda_Dehazing_TV 1e-2 --learn_residual --resize_or_crop crop --display_freq 100 --print_freq 100 --display_port 8090  --epoch_count 1 --niter 90 --niter_decay 0 --fineSize 256 --no_html --batchSize 2   --gpu_id 3 --update_ratio 1 --unlabel_decay 0.99 --save_epoch_freq 1 --model RDehazingnet --g_s2r_premodel ./checkpoints/run_cyclegan/netG_A.pth  
```

3. Train Fs using the pretrained CycleGAN
```
python train.py  --dataroot ./datasets/dehazing --name run_fs_depth --lambda_Dehazing 10 --lambda_Dehazing_DC 1e-2 --lambda_Dehazing_TV 1e-2 --learn_residual --resize_or_crop crop --display_freq 100 --print_freq 100 --display_port 8094  --epoch_count 1 --niter 90 --niter_decay 0 --fineSize 256 --no_html --batchSize 2   --gpu_id 3 --update_ratio 1 --unlabel_decay 0.99 --save_epoch_freq 1 --model SDehazingnet --g_r2s_premodel ./checkpoints/run_cyclegan/netG_B.pth 
```

4. Train DA_dehazing using the pretrained Fr, Fs and CycleGAN.
```
python train.py  --dataroot ./datasets/dehazing --name run_danet_depth --epoch_count 1 --niter 50 --lambda_S 1 --lambda_R 1 --lambda_identity 0.1 --lambda_Dehazing 10 --lambda_Dehazing_Con 0.1 --lambda_Dehazing_DC 1e-2 --lambda_Dehazing_TV 1e-3 --learn_residual --resize_or_crop crop --display_freq 100 --print_freq 100 --display_port 8094 --niter_decay 0 --fineSize 256 --no_html --batchSize 2   --gpu_id 3 --update_ratio 1 --unlabel_decay 0.99 --save_epoch_freq 1 --model danet --S_Dehazing_premodel ./checkpoints/run_fs_depth/netS_Dehazing.pth --R_Dehazing_premodel ./checkpoints/run_fr_depth/netR_Dehazing.pth --g_s2r_premodel ./checkpoints/run_cyclegan_depth/netG_A.pth --g_r2s_premodel ./checkpoints/run_cyclegan/netG_B.pth --d_r_premodel ./checkpoints/run_cyclegan/netD_A.pth --d_s_premodel ./checkpoints/run_cyclegan/netD_B.pth
```
 
## Acknowledgments
Code is inspired by [DA_dahazing](https://github.com/HUSTSYJ/DA_dahazing), [GASDA](https://github.com/sshan-zhao/GASDA) and [CycleGAN](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix).

