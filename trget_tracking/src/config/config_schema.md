# 配置参数结构文档

## TrackerConfig: 追踪器基础配置

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|-----|
| tracker_type | str | MyTracker | 使用的追踪算法类型 |
| confidence_threshold | float | 0.7 | 目标检测置信度阈值 |
| max_miss | int | 5 | 目标丢失最大容忍帧数 |
| input_size | tuple | (640, 480) | 网络输入尺寸 |
| use_gpu | bool | True | 是否使用GPU加速 |
| tracker_input_type_video | bool | True | 追踪器输入类型是否为视频 |
## VideoParams: 视频输入参数配置项

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|-----|
| video_path | str | resources/videos/sample.mp4 | 视频文件路径 |
| begin_frame | int | 15 | 起始检测帧数 |

| video_params | [VideoParams](#videoparams) | <嵌套配置> | 视频参数配置 |

## VideoParams: 视频输入参数配置项

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|-----|
| video_path | str | resources/videos/sample.mp4 | 视频文件路径 |
| begin_frame | int | 15 | 起始检测帧数 |

