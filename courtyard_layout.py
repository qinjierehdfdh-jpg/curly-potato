"""
庭院自动布局系统
基于输入参数实现乡村庭院的智能自动布局
"""

from dataclasses import dataclass
from typing import List, Tuple, Dict, Any
import math
from enum import Enum


class PlantType(Enum):
    """植物类型"""
    TREE = "tree"           # 乔木
    SHRUB = "shrub"         # 灌木
    FLOWER = "flower"       # 花卉
    GRASS = "grass"         # 草坪
    VEGETABLE = "vegetable" # 蔬菜


class StructureType(Enum):
    """建筑结构类型"""
    HOUSE = "house"         # 主房
    SHED = "shed"           # 棚舍
    GATE = "gate"           # 大门
    WELL = "well"           # 水井
    BENCH = "bench"         # 座椅


@dataclass
class Point:
    """二维点"""
    x: float
    y: float
    
    def distance_to(self, other: 'Point') -> float:
        """计算到另一点的距离"""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def __repr__(self):
        return f"({self.x:.1f}, {self.y:.1f})"


@dataclass
class Rectangle:
    """矩形区域"""
    x: float
    y: float
    width: float
    height: float
    
    def contains(self, point: Point) -> bool:
        """检查点是否在矩形内"""
        return (self.x <= point.x <= self.x + self.width and 
                self.y <= point.y <= self.y + self.height)
    
    def overlaps(self, other: 'Rectangle', margin: float = 0) -> bool:
        """检查两个矩形是否重叠"""
        return not (self.x + self.width + margin < other.x or
                   other.x + other.width + margin < self.x or
                   self.y + self.height + margin < other.y or
                   other.y + other.height + margin < self.y)


@dataclass
class LayoutObject:
    """布局对象基类"""
    name: str
    position: Point
    width: float
    height: float
    obj_type: str
    
    def get_bounds(self) -> Rectangle:
        """获取边界矩形"""
        return Rectangle(self.position.x - self.width / 2,
                        self.position.y - self.height / 2,
                        self.width, self.height)


@dataclass
class LayoutParameters:
    """布局参数配置"""
    courtyard_width: float = 20.0      # 庭院宽度 (m)
    courtyard_height: float = 30.0     # 庭院高度 (m)
    
    # 植物参数
    tree_min_spacing: float = 3.0      # 乔木最小间距
    shrub_min_spacing: float = 1.5     # 灌木最小间距
    flower_min_spacing: float = 0.5    # 花卉最小间距
    
    # 主建筑位置
    house_x_offset: float = 0.5        # 主房相对于庭院的X偏移
    house_y_offset: float = 0.5        # 主房相对于庭院的Y偏移
    house_width: float = 6.0           # 主房宽度
    house_height: float = 8.0          # 主房高度
    
    # 功能区参数
    vegetable_area_ratio: float = 0.2  # 蔬菜种植区比例
    recreation_area_ratio: float = 0.15 # 休闲区比例
    
    # 其他参数
    margin: float = 0.5                # 边界边距
    min_path_width: float = 0.8        # 最小通道宽度


class CourtYardLayout:
    """庭院自动布局引擎"""
    
    def __init__(self, params: LayoutParameters = None):
        """初始化布局引擎"""
        self.params = params or LayoutParameters()
        self.objects: List[LayoutObject] = []
        self.structures: List[LayoutObject] = []
        self.available_space: List[Rectangle] = []
        
    def validate_parameters(self) -> bool:
        """验证参数有效性"""
        errors = []
        
        if self.params.courtyard_width <= 0:
            errors.append("庭院宽度必须大于0")
        if self.params.courtyard_height <= 0:
            errors.append("庭院高度必须大于0")
        if self.params.house_width >= self.params.courtyard_width:
            errors.append("主房宽度不能超过庭院宽度")
        if self.params.house_height >= self.params.courtyard_height:
            errors.append("主房高度不能超过庭院高度")
        if not (0 < self.params.vegetable_area_ratio < 1):
            errors.append("蔬菜种植区比例应在0-1之间")
        
        if errors:
            print("参数验证错误:")
            for error in errors:
                print(f"  - {error}")
            return False
        return True
    
    def place_house(self) -> bool:
        """放置主房结构"""
        house_x = self.params.margin + self.params.house_x_offset
        house_y = self.params.margin + self.params.house_y_offset
        
        house_pos = Point(house_x + self.params.house_width / 2,
                         house_y + self.params.house_height / 2)
        
        house = LayoutObject(
            name="主房",
            position=house_pos,
            width=self.params.house_width,
            height=self.params.house_height,
            obj_type=StructureType.HOUSE.value
        )
        
        self.structures.append(house)
        self.objects.append(house)
        
        print(f"✓ 主房已放置: 位置 {house_pos}, 尺寸 {self.params.house_width}m × {self.params.house_height}m")
        return True
    
    def calculate_available_spaces(self) -> List[Rectangle]:
        """计算可用空间"""
        spaces = []
        
        # 初始可用空间为整个庭院
        main_space = Rectangle(
            self.params.margin,
            self.params.margin,
            self.params.courtyard_width - 2 * self.params.margin,
            self.params.courtyard_height - 2 * self.params.margin
        )
        
        # 从可用空间中减去已放置的对象
        remaining_spaces = [main_space]
        
        for obj in self.structures:
            bounds = obj.get_bounds()
            new_spaces = []
            
            for space in remaining_spaces:
                # 如果不重叠，保留该空间
                if not bounds.overlaps(space, margin=self.params.min_path_width):
                    new_spaces.append(space)
                else:
                    # 分割空间
                    split_spaces = self._split_space(space, bounds)
                    new_spaces.extend(split_spaces)
            
            remaining_spaces = new_spaces
        
        return remaining_spaces
    
    def _split_space(self, space: Rectangle, obstacle: Rectangle) -> List[Rectangle]:
        """分割被障碍物切割的空间"""
        spaces = []
        
        # 左侧空间
        if space.x < obstacle.x:
            spaces.append(Rectangle(
                space.x, space.y,
                obstacle.x - space.x, space.height
            ))
        
        # 右侧空间
        if space.x + space.width > obstacle.x + obstacle.width:
            spaces.append(Rectangle(
                obstacle.x + obstacle.width, space.y,
                space.x + space.width - obstacle.x - obstacle.width, space.height
            ))
        
        # 上侧空间
        if space.y < obstacle.y:
            spaces.append(Rectangle(
                space.x, space.y,
                space.width, obstacle.y - space.y
            ))
        
        # 下侧空间
        if space.y + space.height > obstacle.y + obstacle.height:
            spaces.append(Rectangle(
                space.x, obstacle.y + obstacle.height,
                space.width, space.y + space.height - obstacle.y - obstacle.height
            ))
        
        return spaces
    
    def place_plants(self, plant_type: PlantType, count: int) -> int:
        """放置植物"""
        placed = 0
        self.available_space = self.calculate_available_spaces()
        
        if plant_type == PlantType.TREE:
            size = 1.5
            spacing = self.params.tree_min_spacing
        elif plant_type == PlantType.SHRUB:
            size = 1.0
            spacing = self.params.shrub_min_spacing
        elif plant_type == PlantType.FLOWER:
            size = 0.6
            spacing = self.params.flower_min_spacing
        else:
            size = 0.8
            spacing = 0.3
        
        attempts = 0
        max_attempts = count * 10
        
        while placed < count and attempts < max_attempts:
            attempts += 1
            
            # 随机选择可用空间
            if not self.available_space:
                break
            
            space = self.available_space[int(len(self.available_space) * (attempts % len(self.available_space)) / max_attempts)]
            
            # 在空间内随机放置
            x = space.x + (space.width / 2)
            y = space.y + (space.height / 2)
            
            pos = Point(x, y)
            
            # 检查与其他对象的距离
            if self._can_place_object(pos, size, spacing):
                plant = LayoutObject(
                    name=f"{plant_type.value}_{placed + 1}",
                    position=pos,
                    width=size,
                    height=size,
                    obj_type=plant_type.value
                )
                self.objects.append(plant)
                placed += 1
        
        print(f"✓ {plant_type.value}: 已放置 {placed}/{count} 个")
        return placed
    
    def _can_place_object(self, pos: Point, size: float, min_spacing: float) -> bool:
        """检查是否可以放置对象"""
        bounds = Rectangle(pos.x - size / 2, pos.y - size / 2, size, size)
        
        # 检查庭院边界
        if (bounds.x < self.params.margin or 
            bounds.x + bounds.width > self.params.courtyard_width - self.params.margin or
            bounds.y < self.params.margin or
            bounds.y + bounds.height > self.params.courtyard_height - self.params.margin):
            return False
        
        # 检查与其他对象的距离
        for obj in self.objects:
            if pos.distance_to(obj.position) < (size / 2 + obj.width / 2 + min_spacing):
                return False
        
        return True
    
    def create_vegetation_zones(self) -> Dict[str, Rectangle]:
        """创建功能区"""
        zones = {}
        
        # 蔬菜种植区
        veg_area = self.params.courtyard_width * self.params.courtyard_height * self.params.vegetable_area_ratio
        veg_width = self.params.courtyard_width * 0.8
        veg_height = veg_area / veg_width
        
        zones['vegetable'] = Rectangle(
            self.params.margin,
            self.params.courtyard_height - self.params.margin - veg_height,
            veg_width,
            veg_height
        )
        
        # 休闲区
        rec_area = self.params.courtyard_width * self.params.courtyard_height * self.params.recreation_area_ratio
        rec_width = self.params.courtyard_width * 0.6
        rec_height = rec_area / rec_width
        
        zones['recreation'] = Rectangle(
            self.params.courtyard_width - self.params.margin - rec_width,
            self.params.margin,
            rec_width,
            rec_height
        )
        
        return zones
    
    def generate_layout(self) -> Dict[str, Any]:
        """生成完整布局"""
        print("\n" + "="*50)
        print("开始生成庭院自动布局...")
        print("="*50 + "\n")
        
        # 验证参数
        if not self.validate_parameters():
            return None
        
        print(f"庭院尺寸: {self.params.courtyard_width}m × {self.params.courtyard_height}m\n")
        
        # 放置主房
        self.place_house()
        
        # 放置植物
        self.place_plants(PlantType.TREE, 5)
        self.place_plants(PlantType.SHRUB, 8)
        self.place_plants(PlantType.FLOWER, 12)
        
        # 创建功能区
        zones = self.create_vegetation_zones()
        
        # 生成输出
        result = {
            'parameters': self.params.__dict__,
            'objects': [
                {
                    'name': obj.name,
                    'type': obj.obj_type,
                    'position': (obj.position.x, obj.position.y),
                    'size': (obj.width, obj.height)
                }
                for obj in self.objects
            ],
            'zones': {
                key: {
                    'position': (zone.x, zone.y),
                    'size': (zone.width, zone.height)
                }
                for key, zone in zones.items()
            }
        }
        
        print("\n" + "="*50)
        print("布局生成完成！")
        print("="*50 + "\n")
        
        return result
    
    def export_layout_data(self, filepath: str) -> None:
        """导出布局数据为JSON"""
        import json
        
        layout_data = self.generate_layout()
        if layout_data:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(layout_data, f, ensure_ascii=False, indent=2)
            print(f"✓ 布局数据已保存到: {filepath}")
    
    def print_layout_summary(self) -> None:
        """打印布局摘要"""
        print("\n📋 布局对象汇总:")
        print("-" * 60)
        
        obj_types = {}
        for obj in self.objects:
            if obj.obj_type not in obj_types:
                obj_types[obj.obj_type] = []
            obj_types[obj.obj_type].append(obj)
        
        for obj_type, objs in obj_types.items():
            print(f"  {obj_type.upper()}: {len(objs)} 个")
            for obj in objs[:3]:  # 显示前3个
                print(f"    - {obj.name} @ {obj.position}")
            if len(objs) > 3:
                print(f"    ... 和其他 {len(objs) - 3} 个")
        
        print("-" * 60 + "\n")


def example_usage():
    """使用示例"""
    
    # 方案1: 默认参数
    print("\n🏡 方案1: 默认布局")
    layout1 = CourtYardLayout()
    layout1.generate_layout()
    layout1.print_layout_summary()
    
    # 方案2: 自定义参数 - 小型庭院
    print("\n🏡 方案2: 小型庭院布局 (15m × 20m)")
    params2 = LayoutParameters(
        courtyard_width=15,
        courtyard_height=20,
        house_width=4,
        house_height=5,
        tree_min_spacing=2.0,
        vegetable_area_ratio=0.25
    )
    layout2 = CourtYardLayout(params2)
    layout2.generate_layout()
    layout2.print_layout_summary()
    
    # 方案3: 自定义参数 - 大型庭院
    print("\n🏡 方案3: 大型庭院布局 (30m × 40m)")
    params3 = LayoutParameters(
        courtyard_width=30,
        courtyard_height=40,
        house_width=8,
        house_height=10,
        tree_min_spacing=3.5,
        vegetable_area_ratio=0.15,
        recreation_area_ratio=0.2
    )
    layout3 = CourtYardLayout(params3)
    layout3.generate_layout()
    layout3.print_layout_summary()


if __name__ == "__main__":
    example_usage()
