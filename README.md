

# 目标追踪和轨迹绘制

依托项目：[open-mmlab/mmtracking: OpenMMLab Video Perception Toolbox. It supports Video Object Detection (VID), Multiple Object Tracking (MOT), Single Object Tracking (SOT), Video Instance Segmentation (VIS) with a unified framework.](https://github.com/open-mmlab/mmtracking)

trget_tracking/mmtracking/README.md文件里有关于该项目的详细介绍



# 环境配置MMTracking

代码测试环境：GPU RTX4080、CUDA1v12.8

## 查看自己电脑的CUDA版本（安装英伟达显卡）

电脑上搜索命令提示符，用管理员身份运行，然后输入nvidia-smi，显示结果的右上角的CUDA Version便是CUDA Driver API版本

## 创建虚拟环境



## 下载安装pytorch

pip3 install torch==1.12.0+cu113  torchvision==0.12.0+cu113  torchaudio==0.13.0+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html    （根据实际电脑CUDA版本安装对应的pytorch）

torch和torchvision版本对应关系

![image-20250424230006629](C:\Users\aozhi\AppData\Roaming\Typora\typora-user-images\image-20250424230006629.png)

## 下载安装mmcv-full

#先安装mmdet库

pip install mmdet==2.26.0  (一定要3.x版本以下，否则装mmcv-full一定会报错)

#接下来安装mmcv-full

pip install mmcv-full==1.6.2 -f https://download.openmmlab.com/mmcv/dist/cu113/torch1.10.0/index.html 



## 安装MMTracking依赖包

先进入mmtracking目录

cd trget_tracking/mmtracking

pip install -r requirements/build.txt

pip install -v -e .





# 使用

运行trget_tracking/src/main.py文件，然后框选想要进行目标追踪的物体，再按enter键进行目标追踪和轨迹绘制

相关参数位于ObjectTracking\trget_tracking\src\config\settings.py





































