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

# 递归地去除指定的命名空间前缀
def strip_namespace(element):
    if '}' in element.tag:
        element.tag = element.tag.split('}', 1)[1]
    for el in element:
        strip_namespace(el)
    for attr in list(element.attrib.keys()):
        if '}' in attr:
            element.attrib[attr.split('}', 1)[1]] = element.attrib.pop(attr)

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
    
    # 保留根元素的原始属性
    original_attrib = root.attrib.copy()
    
    # 去除命名空间前缀
    strip_namespace(root)
    
    # 恢复根元素的原始属性，并添加xmlns属性
    root.attrib.clear()
    root.attrib.update(original_attrib)
    root.set('xmlns', 'http://www.w3.org/2000/svg')
    
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
            if style.startswith('.st'):
                parts = style.split('{')
                style_name = parts[0]
                color = parts[1].split(':')[1].split(';')[0].strip()
                # 对每个样式的不规律随机抖动
                new_color = randomize_color_to_hsl(color)
                new_styles.append(f'{style_name} {{fill: {new_color};}}')
            else:
                new_styles.append(style)
        
        # 修改样式表
        style_element.text = '\n'.join(new_styles)
        
        # 对circle元素的r属性进行随机抖动
        randomize_circle_radius(root)
        
        # 保存新的SVG文件
        new_file_name = f"{os.path.splitext(file_path)[0]}_{version}.svg"
        tree.write(new_file_name, encoding='utf-8', xml_declaration=True)

# 使用示例
file_path = './public/svg'  # 替换为你的SVG文件路径
process_svg(file_path)
