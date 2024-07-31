import os
import random
from xml.etree import ElementTree as ET
import webcolors
import colorsys

# 随机抖动颜色并转换为HSL格式的函数
def randomize_color_to_hsl(color, hue_amount=50, lightness_amount=50, saturation_amount=50):
    try:
        rgb_color = webcolors.name_to_rgb(color)
    except ValueError:
        try:
            rgb_color = webcolors.hex_to_rgb(color)
        except ValueError:
            try:
                rgb_color = webcolors.rgb_percent_to_rgb(color)
            except ValueError:
                return color  # 返回原始颜色，如果解析失败
    
    r, g, b = rgb_color.red / 255.0, rgb_color.green / 255.0, rgb_color.blue / 255.0
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    # 不规律的随机抖动色相、亮度和饱和度
    h = (h + random.uniform(-hue_amount / 360.0, hue_amount / 360.0)) % 1.0
    l = max(0, min(1, l + random.uniform(-lightness_amount / 255.0, lightness_amount / 255.0)))
    s = max(0, min(1, s + random.uniform(-saturation_amount / 255.0, saturation_amount / 255.0)))
    
    return f'hsl({int(h * 360)}, {int(s * 100)}%, {int(l * 100)}%)'

# 递归地去除命名空间前缀
def strip_namespace(element):
    for el in element.iter():
        if '}' in el.tag:
            el.tag = el.tag.split('}', 1)[1]  # 去掉命名空间URI部分
    return element

# 随机抖动circle元素的r属性
def randomize_circle_radius(element, amount=15):
    for circle in element.findall('.//circle'):
        if 'r' in circle.attrib:
            original_radius = float(circle.attrib['r'])
            change = random.uniform(-amount, amount)
            new_radius = max(0, original_radius + change)
            circle.attrib['r'] = str(new_radius)

# 处理SVG文件
def process_svg(file_path, versions=5):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # 去除命名空间前缀
    root = strip_namespace(root)
    
    # 获取所有样式定义
    style_element = root.find('.//style')
    if style_element is None:
        print(f"No style element found in {file_path}")
        return
    
    styles = style_element.text.strip().split('\n')
    
    # 处理指定的样式
    for version in range(1, versions + 1):
        new_styles = []
        for style in styles:
            if 'fill:' in style:  # 只处理包含fill属性的样式
                parts = style.split('{')
                style_name = parts[0]
                properties = parts[1].rstrip('}').split(';')  # 移除多余的}
                for i, prop in enumerate(properties):
                    if 'fill:' in prop:
                        color = prop.split(':')[1].strip()
                        new_color = randomize_color_to_hsl(color)
                        properties[i] = f'fill: {new_color}'
                new_style = f'{style_name} {{{";".join(properties).strip()};}}'
                new_styles.append(new_style)
            else:
                new_styles.append(style)  # 保留不处理的样式
        
        # 修改样式表
        style_element.text = '\n'.join(new_styles)
        
        # 对circle元素的r属性进行随机抖动
        randomize_circle_radius(root)
        
        # 重新添加命名空间声明
        root.set("xmlns", "http://www.w3.org/2000/svg")
        
        # 保存新的SVG文件
        new_file_name = f"{os.path.splitext(file_path)[0]}_{version}.svg"
        tree.write(new_file_name)

# 使用示例
file_path = './public/testsvg/简版网络图.svg'  # 替换为你的SVG文件路径
process_svg(file_path)
