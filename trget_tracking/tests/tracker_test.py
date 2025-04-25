from trget_tracking.src.app.core.target_tracking_video import TrackerController
from trget_tracking.src.config import *

from mmtrack.apis import init_model,inference_sot # 导入初始化模型的函数
import mmcv
import tempfile


#先运行InitBboxGetting_test.py获得初始检测框,这里直接给出了15帧时的初始检测框
init_bbox = [626, 384, 58, 48]

#实例化参数类
tracker_config = TrackerConfig()
#实例化化追踪器类
tracker_controller = TrackerController(
    tracker_config.sot_config,
    tracker_config.sot_checkpoint,
    tracker_config.device_gpu,
    init_bbox,
    tracker_config.video_tracker.process_video_path,#这里追踪器的输入视频需要为经过剪辑处理后的视频
    tracker_config.video_tracker.output_video_path
)

sot_model = tracker_controller.initialize_tracker()
circle_coord_list =tracker_controller.start_tracking(sot_model)











