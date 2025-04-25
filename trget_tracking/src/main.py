from trget_tracking.src.app.core.target_tracking_video import TrackerController
from trget_tracking.src.config import *
from trget_tracking.src.app.utils import PathUtils
from mmtrack.apis import init_model,inference_sot # 导入初始化模型的函数
import mmcv
import tempfile
from trget_tracking.src.app.utils import *




if __name__ == '__main__':

    #实例化参数类
    tracker_config = TrackerConfig()
    csv_writer_config = CsvWriterConfig()
    camera_params = CameraParams()

#视频预处理模块
    # 选择视频为输入源，获取目标检测框获取器类
    bbox_getter = create_bbox_getter(tracker_input_type_video=True,
                                     video_path=tracker_config.video_tracker.input_video_path,
                                     begin_frame=tracker_config.video_tracker.begin_frame)
    # 获取目标检测框并打印检测框坐标数据
    init_bbox = bbox_getter.get_bounding_box()

    # 实例化视频处理类
    video_processor = VideoProcessor()
    # 进行剪辑处理
    video_processor.trim_video(input_video_path=tracker_config.video_tracker.input_video_path,
                               process_video_path=tracker_config.video_tracker.process_video_path,
                               begin_frame=tracker_config.video_tracker.begin_frame,
                               end_frame=tracker_config.video_tracker.end_frame)


#目标追踪模块
    # 实例化化追踪器类
    tracker_controller = TrackerController(
        tracker_config.sot_config,
        tracker_config.sot_checkpoint,
        tracker_config.device_gpu,
        init_bbox,
        tracker_config.video_tracker.process_video_path,#这里追踪器的输入视频需要为经过剪辑处理后的视频
        tracker_config.video_tracker.output_video_path
    )
    #初始化追踪器
    sot_model = tracker_controller.initialize_tracker()
    #启动追踪器
    circle_coord_list = tracker_controller.start_tracking(sot_model)

# 相机标定模块，获得相机坐标系下的目标中心坐标
    camera_coord_list = []
    for frame_id, x, y in circle_coord_list:
        # 像素坐标转换为相机坐标
        camera_coord = coordinate_pixel2camera((x, y), camera_params.K, camera_params.D, camera_params.depth)
        camera_coord_list.append((frame_id, camera_coord[0], camera_coord[1]))


 
#目标中心坐标记录模块
    # 将目标中心写入csv文件中
    datalogger = DataLogger(output_csv_path = csv_writer_config.output_csv_path,
                            begin_frame = tracker_config.video_tracker.begin_frame,
                            end_frame= tracker_config.video_tracker.end_frame,
                            center_points = camera_coord_list,
                            header = csv_writer_config.header)
    #初始化写入器,完成静态数据处理（处理视频文件，非实时数据）
    datalogger.initialize_writer()



    




