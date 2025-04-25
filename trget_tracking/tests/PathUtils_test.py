'''
包PathUtils测试，是否能获取指定文件绝对路径
'''

from trget_tracking.src.app.utils import PathUtils
import cv2
import os

# 输入文件相对路径，获取绝对路径
video_name = 'ball6.mp4'
path1 = PathUtils.get_absolute_path(relative_path = f'trget_tracking/data/video/input_video/{video_name}')
print(f'视频文件路径:{path1}')

#测试路径是否正确，正确的话则能打开视频文件
cap = cv2.VideoCapture(path1)
if not cap.isOpened():
    print(f"错误：视频文件打开失败")
else:
    print("视频打开成功，开始播放...（按ESC退出）")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Video Preview', frame)
        if cv2.waitKey(25) & 0xFF == 27:  # ESC键
            break
    cap.release()
    cv2.destroyAllWindows()

