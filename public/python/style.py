from lxml import etree
import re

class SVGModifier:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def modify_and_save_svg(self):
        self.load_svg()
        self.embed_css_styles()
        self.save_svg()

    def load_svg(self):
        parser = etree.XMLParser(remove_blank_text=True)
        self.tree = etree.parse(self.input_path, parser)
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

    def save_svg(self):
        self.tree.write(self.output_path, encoding='utf-8', xml_declaration=True, pretty_print=True)

# 使用方法 - 一行代码完成所有操作
SVGModifier('./public/python/svg/不等宽柱状图.svg', './public/newData/9.svg').modify_and_save_svg()
