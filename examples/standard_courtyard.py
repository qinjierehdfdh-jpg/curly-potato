"""
标准乡村庭院布局示例
25m × 35m的均衡型庭院设计
适合一般农村家庭，兼顾植物、蔬菜和休闲功能
"""

from courtyard_layout import CourtYardLayout, LayoutParameters
from layout_visualizer import LayoutVisualizer


def standard_courtyard_example():
    """标准庭院布局示例"""
    
    print("\n" + "="*60)
    print("🏡 标准乡村庭院布局示例")
    print("="*60)
    print("\n📐 庭院规格: 25m × 35m")
    print("👥 适用: 一般农村家庭、均衡布局\n")
    
    # 创建参数
    params = LayoutParameters(
        courtyard_width=25,        # 25米宽
        courtyard_height=35,       # 35米高
        house_width=7,             # 7米宽的主房
        house_height=9,            # 9米高的主房
        house_x_offset=0.8,        # X偏移0.8米
        house_y_offset=0.8,        # Y偏移0.8米
        tree_min_spacing=3.0,      # 乔木间距3米
        shrub_min_spacing=1.5,     # 灌木间距1.5米
        flower_min_spacing=0.5,    # 花卉间距0.5米
        vegetable_area_ratio=0.2,  # 20%用于蔬菜种植
        recreation_area_ratio=0.15 # 15%用于休闲区
    )
    
    # 生成布局
    layout = CourtYardLayout(params)
    layout.generate_layout()
    layout.print_layout_summary()
    
    # 生成可视化
    visualizer = LayoutVisualizer(layout, scale=20)
    
    print("\n📊 生成可视化文件...")
    visualizer.generate_svg('standard_courtyard_layout.svg')
    visualizer.generate_html_report('standard_courtyard_report.html')
    
    print("\n✓ 标准庭院布局设计完成!")
    print("  输出文件:")
    print("  - standard_courtyard_layout.svg")
    print("  - standard_courtyard_report.html")


if __name__ == "__main__":
    standard_courtyard_example()
