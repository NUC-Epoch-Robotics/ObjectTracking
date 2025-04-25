'''
测试视频处理工具，包括截取
'''
from trget_tracking.src.app.utils import PathUtils
import mmcv
import os
import tempfile

from trget_tracking.src.app.utils import VideoProcessor

input_video_path = PathUtils.get_absolute_path(relative_path = 'trget_tracking/data/video/input_video/ball6.mp4')
#处理后的视频存放路径
process_video_path = PathUtils.get_absolute_path(relative_path = 'trget_tracking/data/video/process_video/ball6.mp4')

#实例化视频处理类
video_processor = VideoProcessor()
#进行剪辑处理
video_processor.trim_video(input_video_path, process_video_path, begin_frame = 15, end_frame = 80)




