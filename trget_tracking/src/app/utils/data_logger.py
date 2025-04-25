import csv
import datetime
from contextlib import contextmanager

class DataLogger:
    def __init__(self, output_csv_path, begin_frame, end_frame, center_points, header):
        self.output_csv_path = output_csv_path
        self.begin_frame = begin_frame  # 保存 begin_frame
        self.end_frame = end_frame
        self.center_points = center_points # 接收三元组列表 (frame_num, circle_x, circle_y)
        self.header = header
        self._file = None
        self._writer = None

    def initialize_writer(self):
        if self._file is not None and not self._file.closed:
            self._file.close()  # 关闭之前的文件句柄

        self._file = open(self.output_csv_path, 'w', newline='')
        self._writer = csv.writer(self._file)
        self._writer.writerow(self.header)
        
        # 使用 begin_frame 作为起始帧号
        for idx,  point in enumerate(self.center_points):
            # 解包为 (frame_num, x, y)
            frame_num, circle_x, circle_y = point
            frame_num = self.begin_frame + idx
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            # 插入 timestamp 到数据行
            self._writer.writerow([frame_num, circle_x, circle_y, timestamp])

        # 添加成功提示
        print(f"\033[92mSuccessfully created CSV file at {self.output_csv_path}, recording frames from {self.begin_frame} to {self.end_frame}.\033[0m")



#实时追踪或需要增量更新的场景
    @contextmanager
    def log_session(self):
        try:
            self._initialize_writer()
            yield
        finally:
            if self._file and not self._file.closed:
                self._file.close()

    def log_data(self, data_tuple):
        if self._writer is None:
            raise RuntimeError("Logger not initialized. Call within log_session context.")
        
        frame_num, circle_x, circle_y = data_tuple
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        # 插入 timestamp 到数据行
        self._writer.writerow([frame_num, circle_x, circle_y, timestamp])