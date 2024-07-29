from lxml import etree
import re
import os

class SVGModifier:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def modify_and_save_svgs(self):
        files = os.listdir(self.input_dir)
        svg_files = [f for f in files if f.endswith('.svg')]
        for idx, file_name in enumerate(svg_files, 1):
            input_path = os.path.join(self.input_dir, file_name)
            output_path = os.path.join(self.output_dir, f'{idx}.svg')
            self.modify_and_save_svg(input_path, output_path)

    def modify_and_save_svg(self, input_path, output_path):
        self.load_svg(input_path)
        self.embed_css_styles()
        self.save_svg(output_path)

    def load_svg(self, input_path):
        parser = etree.XMLParser(remove_blank_text=True)
        self.tree = etree.parse(input_path, parser)
        self.root = self.tree.getroot()
        self._remove_namespace()

    def _remove_namespace(self):
        for elem in self.root.getiterator():
            if not hasattr(elem.tag, 'find'):
                continue
            i = elem.tag.find('}')
            if i >= 0:
                elem.tag = elem.tag[i + 1:]

    def embed_css_styles(self):
        style_element = self.root.find('style')
        if style_element is not None:
            css_text = style_element.text.strip()
            self.root.remove(style_element)
            css_rules = re.findall(r'\.(st\d+)\{([^\}]+)\}', css_text)
            for cls, style in css_rules:
                elements = self.root.xpath(f"//*[@class='{cls}']")
                for elem in elements:
                    existing_style = elem.attrib.get('style', '')
                    new_style = f"{existing_style} {style}".strip()
                    elem.attrib['style'] = new_style
                    if 'class' in elem.attrib:
                        del elem.attrib['class']

    def save_svg(self, output_path):
        self.tree.write(output_path, encoding='utf-8', xml_declaration=True, pretty_print=True)

# 使用新方法批量处理SVG文件
svg_modifier = SVGModifier('./public/svg', './public/newData').modify_and_save_svgs()
