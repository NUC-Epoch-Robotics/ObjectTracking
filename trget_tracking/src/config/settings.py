
'''
参数配置文件
'''

from pydantic import BaseModel, Field
from  trget_tracking.src.app.utils import PathUtils #获取绝对路径
from typing import List



'追踪器配置项 -------------------------------------------------------------------------------------'

video_name: str = 'ball6.mp4'

class VideoTrackerConfig(BaseModel):
    ''' 视频追踪器参数配置类 '''
    
    input_video_path: str = Field(PathUtils.get_absolute_path(f'trget_tracking/data/video/input_video/{video_name}'),
                                                                             description='输入视频文件绝对路径')

    process_video_path: str = Field(PathUtils.get_absolute_path(f'trget_tracking/data/video/process_video/{video_name}'),
                                                                             description='经剪辑处理后的原视频存放路径')
    output_video_path: str = Field(PathUtils.get_absolute_path(f'trget_tracking/data/video/output_video/{video_name}'),
                                                                             description='视频输出目录的绝对路径')
    begin_frame: int = Field(15, description='起始检测帧')
    end_frame: int = Field(70, description='终止检测帧')


class CameraParams(BaseModel):
    ''' 相机内参矩阵配置项 '''
    K: List[List[float]] = Field(
        default=[[602.7175003324863, 0, 351.305582038406],
                [0, 601.6330312976042, 240.0929104708551],
                [0, 0, 1]],
        description='相机内参矩阵，包括相机的焦距和主点坐标'
    )
    D: List[float] = Field(
        default=[0.06712174262966401, -0.2636999208734844,
                0.006484443443073637, 0.01111161327049835, 0],
        description='相机畸变参数，用于图像校正'
    )

    depth: float = Field(1.0, description='目标深度(米)')

    


class CameraTrackerConfig(BaseModel):
    ''' 相机追踪器配置项 '''
    camera_params: CameraParams = Field(
        default_factory=CameraParams,
        description='相机内参配置项'
    )


class TrackerConfig(BaseModel):
    ''' 追踪器基础配置 '''

    device_gpu: str = Field("cuda:0", description='默认使用GPU加速训练，改为cuda:1则用cpu训练')
    tracker_input_type_video: bool = Field(True, description='追踪器输入类型是否为视频，True为视频，False为相机')    
    sot_config: str = Field(PathUtils.get_absolute_path("trget_tracking/mmtracking/configs/sot/siamese_rpn/siamese_rpn_r50_20e_lasot.py"),
                                                                 description='sot算法配置文件路径')
    sot_checkpoint: str = Field(PathUtils.get_absolute_path("trget_tracking/mmtracking/checkpoints/siamese_rpn_r50_1x_lasot_20211203_151612-da4b3c66.pth"),
                                                                 description='sot算法权重文件路径')

    '''追踪器类型配置项 '''
    video_tracker: VideoTrackerConfig = Field(VideoTrackerConfig(), description='视频追踪器参数配置类')
    camera_tracker: CameraTrackerConfig = Field(CameraTrackerConfig(), description='相机追踪器参数配置类')

    



'csv写入器配置项 -------------------------------------------------------------------------------------'
class CsvWriterConfig(BaseModel):
    ''' csv写入器配置类 '''
    output_csv_path: str = Field(PathUtils.get_absolute_path(f"trget_tracking/data/csv/{video_name}.csv"),
                                                                description='输出csv文件绝对路径')
    header: list = Field(["frame", "circle_x", "circle_y" ,"timestamp"], description='csv文件表头，这里记录的是帧号，目标中心，时间戳')





# '文档生成类 -------------------------------------------------------------------------------------'
# import inspect
# from typing import Type

# MD_HEADER = """# 配置参数结构文档\n\n"""

# class SchemaGenerator:
#     def __init__(self):
#         self.lines = [MD_HEADER]

#     def add_model_section(self, model: Type[BaseModel]):
#         class_doc = model.__doc__.strip().replace('\n', ' ') if model.__doc__ else ''
#         self.lines.append(f"## {model.__name__}: {class_doc}\n\n")
        
#         self.lines.append("| 字段 | 类型 | 默认值 | 说明 |\n")
#         self.lines.append("|------|------|--------|-----|\n")

#         for name, field in model.__fields__.items():
#             field_info = field.field_info
#             # 处理嵌套模型字段
#             if hasattr(field.type_, '__origin__') and field.type_.__origin__ == list:
#                 type_name = 'List'
#             elif issubclass(field.type_, BaseModel):
#                 type_name = f"[{field.type_.__name__}](#{field.type_.__name__.lower()})"
#                 self.add_model_section(field.type_)
#             else:
#                 type_name = field.type_.__name__

#             default_str = str(field.default) if field.default is not None else ""
#             self.lines.append(
#                 f"| {name} | {type_name} | {default_str} | {field_info.description} |\n"
#             )
#         self.lines.append("\n")

#     def save(self, path: str):
#         os.makedirs(os.path.dirname(path), exist_ok=True)
#         with open(path, 'w', encoding='utf-8') as f:
#             f.writelines(self.lines)

# if __name__ == "__main__":
#     generator = SchemaGenerator()
#     generator.add_model_section(TrackerConfig)
#     generator.add_model_section(VideoParams)
#     generator.save(os.path.abspath("config_schema.md"))
