'''
视频剪辑处理，裁剪从指定起始帧到结束帧的视频并另存为
'''


import mmcv
import tempfile
import os

class VideoProcessor:
    '''
    process_video_path:经过剪辑处理后的输出视频的路径
    '''

    def trim_video(self,input_video_path, process_video_path, begin_frame, end_frame=None):
        # 输入文件校验
        if not os.path.exists(input_video_path):
            print("\033[91m错误：输入视频文件不存在！\033[0m")
            return

        # 创建临时目录存放帧序列
        with tempfile.TemporaryDirectory() as tmp_dir:
            # 读取视频并截取指定帧范围
            video = mmcv.VideoReader(input_video_path)
            
            # 获取视频总帧数
            total_frames = len(video)
            # 设置默认结束帧
            end_frame = end_frame if end_frame is not None else total_frames - 1
            
            # 打印视频信息
            print(f"\033[93m原视频总帧数：{total_frames} | 帧率：{video.fps}FPS\033[0m")
            print(f"\033[93m剪辑范围：起始帧 {begin_frame} 至 结束帧 {end_frame}\033[0m")
            
            # 创建进度条
            prog_bar = mmcv.ProgressBar(end_frame - begin_frame + 1)
            
            frame_counter = 0
            for i, frame in enumerate(video):
                if i < begin_frame:
                    continue
                if i > end_frame:
                    break
                
                # 使用六位零填充命名帧文件
                mmcv.imwrite(frame, os.path.join(tmp_dir, f'{frame_counter:06d}.jpg'))
                frame_counter += 1
                prog_bar.update()
            
            # 确保输出目录存在
            os.makedirs(os.path.dirname(process_video_path), exist_ok=True)
            
            # 将帧序列转换为视频
            mmcv.frames2video(
                tmp_dir,
                os.path.abspath(process_video_path),  
                fps=video.fps,
                fourcc='mp4v',
                filename_tmpl='{:06d}.jpg'
            )
            
            print(f"\033[92m视频剪辑处理完成！输出视频已保存至：{process_video_path}\033[0m")



        return None