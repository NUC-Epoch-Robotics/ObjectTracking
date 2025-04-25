
'''
相机标定：用于将像素坐标转换为相机坐标系下的二维坐标
'''
import cv2  
import numpy as np  

# 定义一个函数px2xy，用于将像素坐标转换为相机坐标系下的二维坐标
# Define a function px2xy to convert pixel coordinates to 2D coordinates in camera coordinate system
def coordinate_pixel2camera(pixel_point, camera_k, camera_d, depth):
    '''
    pixel_point: 像素坐标系下的坐标，格式为[x, y]，其中x和y分别表示像素坐标的水平和垂直方向
    camera_k: 相机内参矩阵，包括相机的焦距和主点坐标
    camera_d: 相机畸变参数，包括径向畸变和切向畸变
    '''
     
    # 将相机内参矩阵K和相机畸变参数D转换为NumPy数组
    # Convert camera intrinsic matrix K and camera distortion parameters D to NumPy arrays
    MK = np.array(camera_k, dtype=float).reshape(3, 3)
    MD = np.array(camera_d, dtype=float)
    
    # 将输入的像素坐标点转换为NumPy数组
    # Convert the input pixel coordinate point to a NumPy array
    point = np.array(pixel_point, dtype=float).reshape(-1, 1, 2)
    
    # 使用OpenCV的cv2.undistortPoints函数对输入点进行畸变矫正，并乘以深度值depth
    # Use OpenCV's cv2.undistortPoints function to correct distortion of input points and multiply by depth value z
    camera_coord_xy = cv2.undistortPoints(point, MK, MD) * depth
    
    # 返回相机坐标系下的二维坐标
    # Return 2D coordinates in the camera coordinate system
    return camera_coord_xy[0][0]

# 调用函数并打印结果（如果需要）
# Call the function and print the result (if needed)
# print(px2xy([0, 0], K, D, 1))