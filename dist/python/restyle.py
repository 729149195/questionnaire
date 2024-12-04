from lxml import etree

class SVGStyleEmbedder:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.namespace = 'http://www.w3.org/2000/svg'
        self.nsmap = {None: self.namespace}

    def embed_and_save_svg(self):
        self.load_svg()
        self.extract_and_embed_styles()
        self.save_svg()

    def load_svg(self):
        parser = etree.XMLParser(remove_blank_text=True)
        self.tree = etree.parse(self.input_path, parser)
        self.root = self.tree.getroot()

    def extract_and_embed_styles(self):
        style_map = {}
        class_counter = 0
        attributes_of_interest = ['fill', 'stroke', 'stroke-width', 'opacity']  # 可以根据需求添加更多属性

        for elem in self.root.iter():
            style_string = elem.attrib.get('style', '').strip()
            for attr in attributes_of_interest:
                if attr in elem.attrib:
                    style_string += f" {attr}:{elem.attrib[attr]};"
                    del elem.attrib[attr]

            style_string = style_string.strip()
            if not style_string:
                continue

            if style_string not in style_map:
                class_name = f"st{class_counter}"
                style_map[style_string] = class_name
                class_counter += 1
            else:
                class_name = style_map[style_string]

            elem.set('class', class_name)
            if 'style' in elem.attrib:
                del elem.attrib['style']

        css_rules = [f".{cls} {{{style}}}" for style, cls in style_map.items()]
        style_text = '\n'.join(css_rules)
        style_element = etree.Element(f"{{{self.namespace}}}style", nsmap=self.nsmap)
        style_element.text = style_text
        self.root.insert(0, style_element)

    def save_svg(self):
        self.tree.write(self.output_path, encoding='utf-8', xml_declaration=True, pretty_print=True)

# 使用方法
SVGStyleEmbedder('./public/svg/子弹图.svg', './public/svg/子弹图.svg').embed_and_save_svg()