"""
处理与追踪相关的请求，包括初始化追踪器和启动追踪。
假设已经对视频完成了剪辑，现在开始进行目标追踪
"""

from mmtrack.apis import init_model,inference_sot # 导入初始化模型的函数
import mmcv
import tempfile
import os
import cv2


class TrackerController:
    def __init__(self,sot_config,sot_checkpoint,device,init_bbox,input_video_path,output_video_path):
        self.sot_config = sot_config
        self.sot_checkpoint = sot_checkpoint
        self.device = device

        # 初始化边界框转换,从(x, y, width, height)转换为(x1, y1, x2, y2)
        self.init_bbox = [
            init_bbox[0], 
            init_bbox[1], 
            init_bbox[0] + init_bbox[2], 
            init_bbox[1] + init_bbox[3]
        ]
    
        self.output_video_path = output_video_path

        # 视频读取，添加进度条显示
        self.video_reader = mmcv.VideoReader(input_video_path)
        self.progress_bar = mmcv.ProgressBar(len(self.video_reader))
        self.end_frame = len(self.video_reader)  # 自动获取视频总帧数

    def initialize_tracker(self):
        return init_model(self.sot_config, self.sot_checkpoint, self.device)

    def start_tracking(self, sot_model):
        print("开始目标追踪任务，请稍等....")
        # 初始化目标中心坐标列表
        circle_coord_list = []
        
        # 创建临时目录用于保存帧，程序运行完毕后自动删除
        with tempfile.TemporaryDirectory() as temp_dir:
            # 处理视频帧序列
            for frame_idx, frame in enumerate(self.video_reader):
                # 执行目标追踪
                result = inference_sot(sot_model, frame, self.init_bbox, frame_id=frame_idx)
                
                # 记录目标中心坐标
                result_int = result['track_bboxes'].astype('uint32')
                circle_x = int((result_int[0] + result_int[2]) / 2)
                circle_y = int((result_int[1] + result_int[3]) / 2)
                circle_coord_list.append((frame_idx,circle_x, circle_y))

                #绘制目标中心轨迹
                for each in circle_coord_list:
                    cv2.circle(frame, (each[1], each[2]), 5, (0, 0, 255), -1)

                # 保存可视化结果
                sot_model.show_result(
                    frame,
                    result,
                    wait_time=int(1000 / self.video_reader.fps),
                    out_file=os.path.join(temp_dir, f'{frame_idx:06d}.jpg')
                )
                self.progress_bar.update()

            # 生成输出视频
            os.makedirs(os.path.dirname(self.output_video_path), exist_ok=True)  # 修正输出目录路径
            mmcv.frames2video(
                temp_dir, 
                self.output_video_path,
                fps=self.video_reader.fps, 
                fourcc='mp4v'
            )

        print(f"任务完成，输出视频保存至：{self.output_video_path}", end='\n\n')

        return circle_coord_list

           