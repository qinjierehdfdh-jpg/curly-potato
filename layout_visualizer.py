"""
庭院布局可视化模块
将布局数据转换为SVG和HTML报告
"""

from courtyard_layout import CourtYardLayout, LayoutParameters
import json
from datetime import datetime


class LayoutVisualizer:
    """布局可视化器"""
    
    def __init__(self, layout: CourtYardLayout, scale: float = 20):
        """
        初始化可视化器
        
        Args:
            layout: CourtYardLayout 实例
            scale: 缩放比例 (像素/米)
        """
        self.layout = layout
        self.scale = scale
        self.params = layout.params
        
        # 颜色方案
        self.colors = {
            'house': '#CD6E3C',
            'tree': '#2D7A2D',
            'shrub': '#4CAF50',
            'flower': '#E91E63',
            'grass': '#CDDC39',
            'vegetable': '#8BC34A',
            'recreation': '#FFC107',
            'water': '#2196F3',
            'background': '#F5F5DC',
            'path': '#D2B48C'
        }
    
    def to_pixels(self, meters: float) -> float:
        """将米转换为像素"""
        return meters * self.scale
    
    def generate_svg(self, filepath: str = None) -> str:
        """生成SVG格式的布局图"""
        
        width = self.to_pixels(self.params.courtyard_width)
        height = self.to_pixels(self.params.courtyard_height)
        
        svg_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg width="{width + 40}" height="{height + 40}" xmlns="http://www.w3.org/2000/svg">',
            f'  <!-- 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} -->',
            f'  <defs>',
            f'    <style>',
            f'      .courtyard {{ fill: {self.colors["background"]}; stroke: #333; stroke-width: 3; }}',
            f'      .object {{ stroke: #333; stroke-width: 1; }}',
            f'      .zone {{ fill-opacity: 0.1; stroke-width: 2; stroke-dasharray: 5,5; }}',
            f'      .text {{ font-family: Arial, sans-serif; font-size: 10px; }}',
            f'    </style>',
            f'  </defs>',
        ]
        
        # 绘制庭院边界
        svg_lines.append(f'  <!-- 庭院边界 -->')
        svg_lines.append(f'  <rect class="courtyard" x="20" y="20" width="{width}" height="{height}"/>')
        
        # 绘制功能区
        svg_lines.append(f'  <!-- 功能区 -->')
        zones = self.layout.create_vegetation_zones()
        
        for zone_name, zone in zones.items():
            zone_x = self.to_pixels(zone.x) + 20
            zone_y = self.to_pixels(zone.y) + 20
            zone_w = self.to_pixels(zone.width)
            zone_h = self.to_pixels(zone.height)
            
            svg_lines.append(f'  <rect class="zone" x="{zone_x}" y="{zone_y}" width="{zone_w}" height="{zone_h}" fill="{self.colors[zone_name]}"/>')
            
            # 添加区域标签
            label_x = zone_x + zone_w / 2
            label_y = zone_y + zone_h / 2
            zone_label = '蔬菜区' if zone_name == 'vegetable' else '休闲区'
            svg_lines.append(f'  <text class="text" x="{label_x}" y="{label_y}" text-anchor="middle" dominant-baseline="middle" opacity="0.5">{zone_label}</text>')
        
        # 绘制对象
        svg_lines.append(f'  <!-- 布局对象 -->')
        
        # 按类型分组绘制
        object_by_type = {}
        for obj in self.layout.objects:
            if obj.obj_type not in object_by_type:
                object_by_type[obj.obj_type] = []
            object_by_type[obj.obj_type].append(obj)
        
        for obj_type, objs in object_by_type.items():
            color = self.colors.get(obj_type, '#999999')
            
            for obj in objs:
                obj_x = self.to_pixels(obj.position.x) + 20
                obj_y = self.to_pixels(obj.position.y) + 20
                obj_r = self.to_pixels(obj.width / 2)
                
                if obj_type == 'house':
                    # 绘制矩形建筑
                    obj_w = self.to_pixels(obj.width)
                    obj_h = self.to_pixels(obj.height)
                    svg_lines.append(f'  <rect class="object" x="{obj_x - obj_w/2}" y="{obj_y - obj_h/2}" width="{obj_w}" height="{obj_h}" fill="{color}"/>')
                    svg_lines.append(f'  <text class="text" x="{obj_x}" y="{obj_y}" text-anchor="middle" dominant-baseline="middle" fill="white" font-weight="bold">主房</text>')
                else:
                    # 绘制圆形植物
                    svg_lines.append(f'  <circle class="object" cx="{obj_x}" cy="{obj_y}" r="{obj_r}" fill="{color}"/>')
        
        # 添加图例
        legend_x = width + 30
        legend_y = 40
        
        svg_lines.append(f'  <!-- 图例 -->')
        svg_lines.append(f'  <text class="text" x="{legend_x}" y="{legend_y}" font-weight="bold" font-size="12">图例</text>')
        
        legend_items = [
            ('house', '主房'),
            ('tree', '乔木'),
            ('shrub', '灌木'),
            ('flower', '花卉'),
            ('vegetable', '蔬菜区'),
            ('recreation', '休闲区')
        ]
        
        for i, (item_type, item_label) in enumerate(legend_items):
            item_y = legend_y + 25 + i * 20
            color = self.colors.get(item_type, '#999999')
            
            if item_type in ['vegetable', 'recreation']:
                svg_lines.append(f'  <rect x="{legend_x}" y="{item_y - 7}" width="12" height="12" fill="{color}" opacity="0.3" stroke="{color}"/>')
            elif item_type == 'house':
                svg_lines.append(f'  <rect x="{legend_x}" y="{item_y - 7}" width="12" height="12" fill="{color}"/>')
            else:
                svg_lines.append(f'  <circle cx="{legend_x + 6}" cy="{item_y}" r="6" fill="{color}"/>')
            
            svg_lines.append(f'  <text class="text" x="{legend_x + 20}" y="{item_y + 3}">{item_label}</text>')
        
        # 添加统计信息
        stats_y = legend_y + 25 + len(legend_items) * 20 + 20
        object_count = len(self.layout.objects)
        area = self.params.courtyard_width * self.params.courtyard_height
        
        svg_lines.append(f'  <!-- 统计信息 -->')
        svg_lines.append(f'  <text class="text" x="{legend_x}" y="{stats_y}" font-weight="bold" font-size="11">统计</text>')
        svg_lines.append(f'  <text class="text" x="{legend_x}" y="{stats_y + 18}" font-size="10">对象数: {object_count}</text>')
        svg_lines.append(f'  <text class="text" x="{legend_x}" y="{stats_y + 35}" font-size="10">庭院面积: {area:.1f}m²</text>')
        
        svg_lines.append('</svg>')
        
        svg_content = '\n'.join(svg_lines)
        
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            print(f"✓ SVG文件已保存: {filepath}")
        
        return svg_content
    
    def generate_html_report(self, filepath: str = None) -> str:
        """生成HTML交互式报告"""
        
        # 生成SVG
        svg_content = self.generate_svg()
        
        # 生成统计数据
        object_stats = {}
        for obj in self.layout.objects:
            obj_type = obj.obj_type
            if obj_type not in object_stats:
                object_stats[obj_type] = 0
            object_stats[obj_type] += 1
        
        # 参数表
        params_table = self._generate_params_table()
        object_table = self._generate_object_table()
        
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>庭院自动布局报告</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Microsoft YaHei', 'SimHei', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 32px;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 14px;
            opacity: 0.9;
        }}
        
        .content {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            padding: 40px 30px;
        }}
        
        .left-panel {{
            display: flex;
            flex-direction: column;
        }}
        
        .right-panel {{
            display: flex;
            flex-direction: column;
        }}
        
        .svg-container {{
            background: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            flex: 1;
        }}
        
        .section {{
            margin-bottom: 30px;
        }}
        
        .section-title {{
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        
        th {{
            background: #f5f5f5;
            font-weight: bold;
            color: #333;
        }}
        
        tr:hover {{
            background: #f9f9f9;
        }}
        
        .stat-box {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .stat-item {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        
        .stat-item .label {{
            font-size: 12px;
            opacity: 0.9;
            margin-bottom: 8px;
        }}
        
        .stat-item .value {{
            font-size: 28px;
            font-weight: bold;
        }}
        
        .footer {{
            background: #f5f5f5;
            padding: 20px 30px;
            text-align: center;
            color: #666;
            font-size: 12px;
            border-top: 1px solid #ddd;
        }}
        
        @media (max-width: 1200px) {{
            .content {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏡 庭院自动布局设计报告</h1>
            <p>生成时间: {datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")}</p>
        </div>
        
        <div class="content">
            <div class="left-panel">
                <div class="section">
                    <h2 class="section-title">📐 布局平面图</h2>
                    <div class="svg-container">
                        {svg_content}
                    </div>
                </div>
            </div>
            
            <div class="right-panel">
                <div class="section">
                    <h2 class="section-title">📊 统计数据</h2>
                    <div class="stat-box">
                        <div class="stat-item">
                            <div class="label">庭院尺寸</div>
                            <div class="value">{self.params.courtyard_width:.0f}×{self.params.courtyard_height:.0f}m</div>
                        </div>
                        <div class="stat-item">
                            <div class="label">庭院面积</div>
                            <div class="value">{self.params.courtyard_width * self.params.courtyard_height:.0f}m²</div>
                        </div>
                        <div class="stat-item">
                            <div class="label">布局对象数</div>
                            <div class="value">{len(self.layout.objects)}</div>
                        </div>
                        <div class="stat-item">
                            <div class="label">植物总数</div>
                            <div class="value">{len(self.layout.objects) - 1}</div>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2 class="section-title">⚙️ 布局参数</h2>
                    {params_table}
                </div>
                
                <div class="section">
                    <h2 class="section-title">📋 对象统计</h2>
                    <table>
                        <tr>
                            <th>类型</th>
                            <th>数量</th>
                        </tr>
                        {"".join(f'<tr><td>{obj_type}</td><td>{count}</td></tr>' for obj_type, count in sorted(object_stats.items()))}
                    </table>
                </div>
            </div>
        </div>
        
        <div style="padding: 30px; background: #f9f9f9; border-top: 1px solid #ddd;">
            <h2 class="section-title">📍 对象详细信息</h2>
            {object_table}
        </div>
        
        <div class="footer">
            <p>本报告由庭院自动布局系统生成 | 基于参数化设计和智能算法</p>
        </div>
    </div>
</body>
</html>"""
        
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"✓ HTML报告已保存: {filepath}")
        
        return html_content
    
    def _generate_params_table(self) -> str:
        """生成参数表"""
        params_data = [
            ('庭院宽度', f"{self.params.courtyard_width:.1f}m"),
            ('庭院高度', f"{self.params.courtyard_height:.1f}m"),
            ('主房宽度', f"{self.params.house_width:.1f}m"),
            ('主房高度', f"{self.params.house_height:.1f}m"),
            ('乔木最小间距', f"{self.params.tree_min_spacing:.1f}m"),
            ('灌木最小间距', f"{self.params.shrub_min_spacing:.1f}m"),
            ('花卉最小间距', f"{self.params.flower_min_spacing:.1f}m"),
            ('蔬菜区比例', f"{self.params.vegetable_area_ratio*100:.0f}%"),
            ('休闲区比例', f"{self.params.recreation_area_ratio*100:.0f}%"),
        ]
        
        table_html = '<table>'
        table_html += '<tr><th>参数</th><th>值</th></tr>'
        for param_name, param_value in params_data:
            table_html += f'<tr><td>{param_name}</td><td>{param_value}</td></tr>'
        table_html += '</table>'
        
        return table_html
    
    def _generate_object_table(self) -> str:
        """生成对象表"""
        table_html = '<table>'
        table_html += '<tr><th>名称</th><th>类型</th><th>位置(X,Y)</th><th>尺寸</th></tr>'
        
        for obj in self.layout.objects[:20]:  # 显示前20个
            x, y = obj.position.x, obj.position.y
            size = f"{obj.width:.2f}m"
            table_html += f'<tr><td>{obj.name}</td><td>{obj.obj_type}</td><td>({x:.1f}, {y:.1f})</td><td>{size}</td></tr>'
        
        if len(self.layout.objects) > 20:
            table_html += f'<tr><td colspan="4" style="text-align: center; color: #999;">... 还有 {len(self.layout.objects) - 20} 个对象</td></tr>'
        
        table_html += '</table>'
        
        return table_html


def example_visualization():
    """可视化示例"""
    
    # 创建布局
    params = LayoutParameters(
        courtyard_width=25,
        courtyard_height=35,
        house_width=7,
        house_height=9,
        tree_min_spacing=3.0
    )
    
    layout = CourtYardLayout(params)
    layout.generate_layout()
    
    # 生成可视化
    visualizer = LayoutVisualizer(layout)
    
    # 保存SVG
    visualizer.generate_svg('courtyard_layout.svg')
    
    # 保存HTML报告
    visualizer.generate_html_report('courtyard_layout_report.html')
    
    print("\n✓ 可视化文件生成完成!")
    print("  - courtyard_layout.svg")
    print("  - courtyard_layout_report.html")


if __name__ == "__main__":
    example_visualization()
