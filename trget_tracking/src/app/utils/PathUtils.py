'''
获取绝对路径的工具类，用于处理项目中的文件路径。
'''

import os
from pathlib import Path

class PathUtils:
    @staticmethod
    def get_project_root():
        """
        获取项目根目录路径（rc_basketball_python目录）
        """
        current_path = Path(__file__).absolute()
        # 向上定位到trget_tracking的父目录
        while 'trget_tracking' in current_path.parts:
            current_path = current_path.parent
        return str(current_path)

    @staticmethod
    def safe_join(base_path, *paths):
        return os.path.abspath(os.path.join(base_path, *paths)).replace('\\', '/')

    @staticmethod
    def get_absolute_path(relative_path):
        root = PathUtils.get_project_root()
        return PathUtils.safe_join(root, relative_path)

    @staticmethod
    def get_file_dir(file_path):
        return os.path.dirname(os.path.abspath(file_path))
