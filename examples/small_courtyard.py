"""
小型家庭庭院布局示例
12m × 18m的紧凑型庭院设计
适合小家庭，优化利用空间，增加蔬菜种植面积
"""

from courtyard_layout import CourtYardLayout, LayoutParameters
from layout_visualizer import LayoutVisualizer


def small_courtyard_example():
    """小型庭院布局示例"""
    
    print("\n" + "="*60)
    print("🏡 小型家庭庭院布局示例")
    print("="*60)
    print("\n📐 庭院规格: 12m × 18m")
    print("👥 适用: 小家庭、紧凑型布局\n")
    
    # 创建参数
    params = LayoutParameters(
        courtyard_width=12,        # 12米宽
        courtyard_height=18,       # 18米高
        house_width=4,             # 4米宽的主房
        house_height=6,            # 6米高的主房
        tree_min_spacing=2.0,      # 乔木间距较小
        shrub_min_spacing=1.2,     # 灌木间距较小
        flower_min_spacing=0.4,    # 花卉间距较小
        vegetable_area_ratio=0.3,  # 30%用于蔬菜种植
        recreation_area_ratio=0.1  # 10%用于休闲区
    )
    
    # 生成布局
    layout = CourtYardLayout(params)
    layout.generate_layout()
    layout.print_layout_summary()
    
    # 生成可视化
    visualizer = LayoutVisualizer(layout, scale=25)
    
    print("\n📊 生成可视化文件...")
    visualizer.generate_svg('small_courtyard_layout.svg')
    visualizer.generate_html_report('small_courtyard_report.html')
    
    print("\n✓ 小型庭院布局设计完成!")
    print("  输出文件:")
    print("  - small_courtyard_layout.svg")
    print("  - small_courtyard_report.html")


if __name__ == "__main__":
    small_courtyard_example()
