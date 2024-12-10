import xml.etree.ElementTree as ET
from CreateGM import GM
import Gestalt_Edges_Features as Gestalt_Edges_Features
# from Statisticians import LayerDataExtractor
import re
import os
from tqdm import tqdm
import json


class LayerDataExtractor:
    def __init__(self, input_path, output_path):
        self.input_path = input_path  # Input file path
        self.output_path = output_path  # Output file path

    def process(self):
        data = self._load_data()
        layer_data = self._extract_layers(data)
        # Creating a single top-level object instead of wrapping the array in an object
        structured_data = self._create_single_top_level_object(layer_data)
        self._save_data(structured_data)

    def _load_data(self):
        # Load JSON file
        with open(self.input_path, 'r') as file:
            return json.load(file)

    def _extract_layers(self, data):
        # Extract layer data for each node
        layer_data = []
        for node_id, node_data in data.items():
            if 'layer' in node_data:
                layer_info = {
                    'id': node_id,
                    'layer': node_data['layer']
                }
                layer_data.append(layer_info)
        return layer_data

    def _create_single_top_level_object(self, data):
        # Create a single top-level object with a "name" and "children" structure
        structure = {"name": "flare", "children": []}  # Assuming top-level name is "flare"
        current_level = structure["children"]

        for item in data:
            layers = item["layer"]
            if not layers:  # If no layer info, add node directly under "flare"
                current_level.append({"name": item["id"], "value": 1})
                continue

            current_level = structure["children"]
            for layer in layers[:-1]:  # Iterate to the second last element
                found = False
                for child in current_level:
                    if child.get("name") == layer:
                        current_level = child.get("children", [])
                        found = True
                        break
                if not found:
                    new_node = {"name": layer, "children": []}
                    current_level.append(new_node)
                    current_level = new_node["children"]

            # Handle the last element, add as a node with "value"
            current_level.append({"name": item["id"], "value": 1})

        return structure

    def _save_data(self, structured_data):
        # Save the structured data to a new JSON file
        with open(self.output_path, 'w') as file:
            json.dump(structured_data, file, indent=4)


class SVGParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.existing_tags = {}

    @staticmethod
    def escape_text_content(svg_content):
        def replacer(match):
            text_with_tags = match.group(0)
            start_tag_end = text_with_tags.find('>') + 1
            end_tag_start = text_with_tags.rfind('<')
            text_content = text_with_tags[start_tag_end:end_tag_start]
            escaped_content = SVGParser.escape_special_xml_chars(text_content)
            return text_with_tags[:start_tag_end] + escaped_content + text_with_tags[end_tag_start:]

        return re.sub(r'<text[^>]*>.*?</text>', replacer, svg_content, flags=re.DOTALL)

    @staticmethod
    def escape_special_xml_chars(svg_content):
        svg_content = re.sub(r'&(?!(amp;|lt;|gt;|quot;|apos;))', '&amp;', svg_content)
        return svg_content

    @staticmethod
    def parse_svg(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            svg_content = file.read()
        svg_content = SVGParser.escape_text_content(svg_content)
        tree = ET.ElementTree(ET.fromstring(svg_content))
        root = tree.getroot()
        return tree, root

    def extract_element_info(self, element):
        tag_with_namespace = element.tag
        tag_without_namespace = tag_with_namespace.split("}")[-1]

        if tag_without_namespace != "svg":
            count = self.existing_tags.get(tag_without_namespace, 0)
            full_tag = (
                f"{tag_without_namespace}_{count}"
                if count > 0
                else tag_without_namespace
            )
            self.existing_tags[tag_without_namespace] = count + 1
        else:
            full_tag = tag_without_namespace

        attributes = element.attrib
        text_content = element.text.strip() if element.text else None

        if text_content:
            element.text = 'x' * len(text_content)
        
        return full_tag, attributes, element.text

    def build_graph(self, svg_root):
        def add_element_to_graph(element, parent_path='svg', level=0, layer="0"):
            tag, attributes, text_content = self.extract_element_info(element)
            node_id = tag

            element.set('id', node_id)

            new_layer_counter = 0
            for child in reversed(element):
                child_layer = f"{layer}_{new_layer_counter}"
                add_element_to_graph(child, parent_path=node_id, level=level + 1, layer=child_layer)
                new_layer_counter += 1

        add_element_to_graph(svg_root)

    def run(self):
        tree, svg_root = SVGParser.parse_svg(self.file_path)
        self.build_graph(svg_root)
        for elem in svg_root.iter():
            elem.tag = elem.tag.split('}', 1)[-1]
            attribs = list(elem.attrib.items())
            for k, v in attribs:
                if k.startswith('{'):
                    del elem.attrib[k]
                    elem.attrib[k.split('}', 1)[-1]] = v
        return tree

def svgid(svg_input_path, svg_output_path):
    parser = SVGParser(svg_input_path)
    svg_tree = parser.run()
    svg_tree.write(svg_output_path, encoding='utf-8', xml_declaration=True)

def ensure_directory_exists(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

for n in tqdm(range(1, 54), desc="Processing SVG files"):
    input_svg_path = f'./public/newData/{n}.svg'
    output_svg_path = f'./public/Data2/{n}/{n}.svg'
    layer_data_path = f'./public/Data2/{n}/layer_data.json'
    output_dir = f'./public/Data2/{n}'

    ensure_directory_exists(output_svg_path)
    ensure_directory_exists(layer_data_path)

    parser = GM(input_svg_path) 
    parser.run()

    Gestalt_Edges_Features.extract_nodes()

    svgid(input_svg_path, output_svg_path)
    
    extractor = LayerDataExtractor('./public/python/data/GMinfo.json', layer_data_path)
    extractor.process()
