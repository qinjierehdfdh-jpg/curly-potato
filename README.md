# 🏡 庭院自动布局系统

基于院落平面图的生成式乡村庭院自动布局系统

![Python](https://img.shields.io/badge/Python-3.7+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 📋 项目描述

这是一个智能化的庭院布局设计系统，通过输入参数（庭院尺寸、建筑位置、植物间距等），系统能够自动生成合理的庭院布局方案。

### ✨ 核心特性

- ✅ **参数化设计** - 通过灵活的参数配置生成不同规模的布局
- ✅ **多植物类型** - 支持乔木、灌木、花卉、蔬菜等多种植物
- ✅ **智能避碰** - 基于距离和碰撞检测确保对象不重叠
- ✅ **功能区规划** - 自动划分蔬菜种植区和休闲区
- ✅ **可视化输出** - 生成SVG矢量图和HTML交互式报告
- ✅ **完整数据导出** - 支持JSON格式的结构化数据输出

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/qinjierehdfdh-jpg/curly-potato.git
cd curly-potato

# 无需额外依赖，Python 3.7+即可运行
```

### 基础使用

```python
from courtyard_layout import CourtYardLayout, LayoutParameters
from layout_visualizer import LayoutVisualizer

# 1. 创建布局引擎（使用默认参数）
layout = CourtYardLayout()
layout.generate_layout()

# 2. 生成可视化
visualizer = LayoutVisualizer(layout)
visualizer.generate_html_report('report.html')
```

### 自定义参数

```python
# 创建自定义参数
params = LayoutParameters(
    courtyard_width=25,        # 庭院宽度(米)
    courtyard_height=35,       # 庭院高度(米)
    house_width=7,             # 主房宽度(米)
    house_height=9,            # 主房高度(米)
    tree_min_spacing=3.0,      # 乔木最小间距(米)
    shrub_min_spacing=1.5,     # 灌木最小间距(米)
    flower_min_spacing=0.5,    # 花卉最小间距(米)
    vegetable_area_ratio=0.2,  # 蔬菜区比例
    recreation_area_ratio=0.15 # 休闲区比例
)

# 使用自定义参数生成布局
layout = CourtYardLayout(params)
layout.generate_layout()
```

## 📊 布局参数详解

### 庭院基本参数

| 参数名 | 类型 | 默认值 | 说明 |
|-------|------|--------|------|
| `courtyard_width` | float | 20.0 | 庭院宽度(米) |
| `courtyard_height` | float | 30.0 | 庭院高度(米) |
| `margin` | float | 0.5 | 庭院边界边距(米) |

### 建筑参数

| 参数名 | 类型 | 默认值 | 说明 |
|-------|------|--------|------|
| `house_width` | float | 6.0 | 主房宽度(米) |
| `house_height` | float | 8.0 | 主房高度(米) |
| `house_x_offset` | float | 0.5 | 主房X方向偏移(米) |
| `house_y_offset` | float | 0.5 | 主房Y方向偏移(米) |

### 植物参数

| 参数名 | 类型 | 默认值 | 说明 |
|-------|------|--------|------|
| `tree_min_spacing` | float | 3.0 | 乔木最小间距(米) |
| `shrub_min_spacing` | float | 1.5 | 灌木最小间距(米) |
| `flower_min_spacing` | float | 0.5 | 花卉最小间距(米) |
| `min_path_width` | float | 0.8 | 最小通道宽度(米) |

### 功能区参数

| 参数名 | 类型 | 默认值 | 说明 |
|-------|------|--------|------|
| `vegetable_area_ratio` | float | 0.2 | 蔬菜种植区占庭院比例 |
| `recreation_area_ratio` | float | 0.15 | 休闲区占庭院比例 |

## 💡 应用场景

### 场景1: 小型家庭庭院

```python
params = LayoutParameters(
    courtyard_width=12,        # 12m×18m的小庭院
    courtyard_height=18,
    house_width=4,
    house_height=6,
    tree_min_spacing=2.0,      # 较小间距
    vegetable_area_ratio=0.3   # 更多蔬菜区
)

layout = CourtYardLayout(params)
layout.generate_layout()
```

**特点**: 紧凑布局，优化利用空间，增加蔬菜种植面积

### 场景2: 标准乡村庭院

```python
params = LayoutParameters(
    courtyard_width=25,
    courtyard_height=35,
    house_width=7,
    house_height=9,
    tree_min_spacing=3.0,
    vegetable_area_ratio=0.2,
    recreation_area_ratio=0.15
)

layout = CourtYardLayout(params)
layout.generate_layout()
```

**特点**: 均衡布局，兼顾植物、蔬菜和休闲功能

### 场景3: 大型豪华庭院

```python
params = LayoutParameters(
    courtyard_width=40,
    courtyard_height=50,
    house_width=10,
    house_height=12,
    tree_min_spacing=4.0,      # 更大间距，更宽敞
    vegetable_area_ratio=0.15, # 较少蔬菜区
    recreation_area_ratio=0.25 # 更多休闲区
)

layout = CourtYardLayout(params)
layout.generate_layout()
```

**特点**: 宽敞布局，强调景观效果和休闲功能

## 📁 项目结构

```
curly-potato/
├── courtyard_layout.py       # 核心布局引擎
├── layout_visualizer.py      # 可视化模块
├── README.md                 # 项目文档
└── examples/
    ├── small_courtyard.py    # 小型庭院示例
    ├── standard_courtyard.py # 标准庭院示例
    └── large_courtyard.py    # 大型庭院示例
```

## 🔧 核心模块说明

### CourtYardLayout 类

主要方法:

- `validate_parameters()` - 验证输入参数有效性
- `place_house()` - 放置主房建筑
- `place_plants(plant_type, count)` - 放置指定类型和数量的植物
- `calculate_available_spaces()` - 计算可用空间
- `create_vegetation_zones()` - 创建功能区
- `generate_layout()` - 生成完整布局
- `export_layout_data(filepath)` - 导出JSON数据

### LayoutVisualizer 类

主要方法:

- `generate_svg(filepath)` - 生成SVG矢量图
- `generate_html_report(filepath)` - 生成HTML交互式报告
- `to_pixels(meters)` - 单位转换

## 📊 输出格式

### 1. HTML报告

交互式可视化报告，包含:
- 📐 平面布局图
- 📊 统计数据（面积、对象数等）
- ⚙️ 参数配置表
- 📋 对象详细信息

生成方式:
```python
visualizer = LayoutVisualizer(layout)
visualizer.generate_html_report('report.html')
```

### 2. SVG矢量图

可缩放矢量图形，包含:
- 庭院边界
- 建筑和植物位置
- 功能区划分
- 图例和统计信息

生成方式:
```python
visualizer = LayoutVisualizer(layout)
visualizer.generate_svg('layout.svg')
```

### 3. JSON数据

结构化数据导出:
```python
layout.export_layout_data('layout.json')
```

输出示例:
```json
{
  "parameters": {
    "courtyard_width": 25,
    "courtyard_height": 35,
    ...
  },
  "objects": [
    {
      "name": "主房",
      "type": "house",
      "position": [12.5, 17.5],
      "size": [7, 9]
    },
    ...
  ],
  "zones": {
    "vegetable": {...},
    "recreation": {...}
  }
}
```

## 🎯 算法原理

### 碰撞检测

系统使用矩形边界盒 (Bounding Box) 进行碰撞检测:

```
两个对象不重叠的条件:
- 对象A右边 < 对象B左边，或
- 对象B右边 < 对象A左边，或
- 对象A下边 < 对象B上边，或
- 对象B下边 < 对象A上边
```

### 距离计算

两个对象间的距离通过欧几里得距离计算:

```
distance = √((x2-x1)² + (y2-y1)²)
```

当 `distance >= (size1/2 + size2/2 + min_spacing)` 时，允许放置

### 空间分割

将被障碍物切割的空间分割成可用的独立区域:
- 左侧空间
- 右侧空间
- 上侧空间
- 下侧空间

## 📈 性能指标

- 算法时间复杂度: O(n²) （n为对象数量）
- 最大支持对象数: 1000+
- 运行时间: <1秒（标准布局）

## 🔍 调试

启用详细日志:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

layout = CourtYardLayout(params)
layout.generate_layout()
```

## 🤝 贡献

欢迎提交 Issues 和 Pull Requests！

## 📄 许可证

MIT License

## 👨‍💻 作者

qinjierehdfdh-jpg

---

**最后更新**: 2026年4月25日

**版本**: 1.0.0
