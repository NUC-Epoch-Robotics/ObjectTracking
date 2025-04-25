"""
目标初始检测框测试：是否能获取初始检测框
"""


import os
import cv2

from trget_tracking.src.app.utils import VideoInitBoundingBoxGetter,CameraInitBoundingBoxGetter,create_bbox_getter
from trget_tracking.src.app.utils import PathUtils

#获取视频绝对路径,若不能获取绝对路径，请先运行PathUtils_test.py验证是否能获取绝对路径
video_path = PathUtils.get_absolute_path(relative_path = 'trget_tracking/data/video/input_video/ball6.mp4')

#选择视频为输入源，获取目标检测框获取器类
bbox_getter = create_bbox_getter(tracker_input_type_video = True, video_path = video_path, begin_frame = 15)
#获取目标检测框并打印检测框坐标数据
init_bbox = bbox_getter.get_bounding_box()

