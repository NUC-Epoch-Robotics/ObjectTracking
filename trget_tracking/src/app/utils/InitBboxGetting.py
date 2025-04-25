"""
用于手动框选需要进行目标追踪的物体，输出为目标的初始检测框，若输入为视频，则可以从指定帧开始获取(已实现)，若输入为摄像头，则实时获取(待实现)
"""


import os
import cv2

from abc import ABC, abstractmethod


class BaseBoundingBoxGetter(ABC):
    """
    目标检测框获取器抽象基类
    
    职责：
    - 定义获取目标检测框的统一接口
    - 规范子类必须实现的选择框获取逻辑
    """
    @abstractmethod
    def get_bounding_box(self):
        """
        抽象方法：获取目标边界框
        
        返回：
            tuple: 包含(x, y, width, height)的元组，表示目标框坐标和尺寸
                 当获取失败时返回None
        """
        pass


class VideoInitBoundingBoxGetter(BaseBoundingBoxGetter):
    def __init__(self, video_path, begin_frame):
        """
        视频源目标框获取器，从指定帧开始获取
        
        参数：
            video_path (str): 视频文件绝对路径
            begin_frame (int): 起始检测帧序号
        """
        self.video_path = video_path
        self.begin_frame = begin_frame
        if begin_frame < 1:
            raise ValueError("起始帧必须大于等于1")
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"视频文件不存在: {video_path}")

        self.frame_width = None
        self.frame_height = None
    def get_bounding_box(self):
        """
        从视频的指定帧开始获取目标框
        
        处理流程：
        1. 初始化视频捕获对象
        2. 跳转到指定起始帧begin_frame
        3. 创建选择窗口并显示目标帧
        4. 捕获用户框选的ROI区域，即需要进行目标追踪的物体
            注意：ROI区域的坐标格式为(x, y, width, height),其中x，y为左上角坐标，width，height为宽度和高度
        5. 打印目标框的坐标信息
        """
        cap = cv2.VideoCapture(self.video_path)
    
        # 获取视频原始尺寸（单位：像素）
        self.frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
        # 跳帧处理：跳过前N-1帧
        for _ in range(self.begin_frame - 1):
            cap.read()

        if cap.isOpened():
            ret, frame = cap.read()
            if ret:

                # 获取视频总帧数
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                
                # 在帧上添加帧号标注
                frame_number = self.begin_frame
                text = f'begin_frame: {frame_number}/total_frame: {total_frames}'
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
                text_x = (self.frame_width - text_size[0]) // 2
                cv2.putText(frame, text, (text_x, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                # 创建可调节窗口
                cv2.namedWindow("initial bbox", cv2.WINDOW_NORMAL)
                cv2.imshow("initial bbox", frame)
                
                # 框选目标物体：返回格式为(x, y, w, h)，其中想x，y为左上角坐标，w，h为宽度和高度
                init_box = cv2.selectROI("initial bbox", frame)
                print(f'获取到初始检测框：x:{init_box[0]} y:{init_box[1]} w:{init_box[2]} h:{init_box[3]}')

                # 清理资源
                cv2.destroyAllWindows()
                cap.release()
                return init_box
            else:
                print("无法读取视频帧")
        else:
            print("视频文件未成功打开")
        cap.release()
        return init_box

class CameraInitBoundingBoxGetter(BaseBoundingBoxGetter):
    def __init__(self):
        """
        摄像头实时目标框获取器
        
        异常：
            当摄像头初始化失败时抛出Exception
        """
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("摄像头初始化失败，请检查设备连接")

    def get_bounding_box(self):
        """
        实时获取目标框
        
        交互逻辑：
        - 按空格键：暂停画面并选择ROI
        - 按ESC键：退出选择
        """
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("摄像头帧读取失败")
                return None
            
            # 实时显示画面
            cv2.namedWindow("实时追踪", cv2.WINDOW_NORMAL)
            cv2.imshow("实时追踪", frame)
            
            # 空格键触发ROI选择
            if cv2.waitKey(1) & 0xFF == 32:
                r = cv2.selectROI("实时追踪", frame)
                
                print(f'检测框坐标格式：{r}')
                cv2.destroyAllWindows()
                self.cap.release()
                return r
            
            # ESC键退出
            if cv2.waitKey(1) & 0xFF == 27:
                self.cap.release()
                return None

def create_bbox_getter(tracker_input_type_video,video_path,begin_frame):
    """
    目标框获取器工厂函数
    根据配置选择合适的目标框获取器
    """
    if tracker_input_type_video:
        video = VideoInitBoundingBoxGetter(video_path, begin_frame)
        return video
    else:
        return CameraInitBoundingBoxGetter()


