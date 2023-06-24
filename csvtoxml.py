# converting the ??? csv file to xml files pascal voc format

import os
import csv
import xml.etree.ElementTree as ET
from PIL import Image

def create_voc_xml(image_filename, objects, image_width, image_height):
    root = ET.Element("annotation")

    folder = ET.SubElement(root, "folder")
    folder.text = os.path.dirname(image_filename)

    filename = ET.SubElement(root, "filename")
    filename.text = os.path.basename(image_filename)

    size = ET.SubElement(root, "size")
    width = ET.SubElement(size, "width")
    height = ET.SubElement(size, "height")
    depth = ET.SubElement(size, "depth")
    width.text = str(image_width)
    height.text = str(image_height)
    depth.text = "3"

    for obj in objects:
        obj_elem = ET.SubElement(root, "object")
        name = ET.SubElement(obj_elem, "name")
        name.text = obj['object_class']

        bndbox = ET.SubElement(obj_elem, "bndbox")
        xmin = ET.SubElement(bndbox, "xmin")
        xmax = ET.SubElement(bndbox, "xmax")
        ymin = ET.SubElement(bndbox, "ymin")
        ymax = ET.SubElement(bndbox, "ymax")

        xmin.text = str(obj['xmin'])
        xmax.text = str(obj['xmax'])
        ymin.text = str(obj['ymin'])
        ymax.text = str(obj['ymax'])

    xml_tree = ET.ElementTree(root)
    return xml_tree

def convert_to_voc_xml(label_file, output_dir):
    with open(label_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        image_objects = {}

        for row in reader:
            image_filename = row['filename']
            object_class = row['object_class']
            xmin = float(row['xmin'])
            xmax = float(row['xmax'])
            ymin = float(row['ymin'])
            ymax = float(row['ymax'])

            # Group objects by image filename
            if image_filename not in image_objects:
                image_objects[image_filename] = []

            objects = image_objects[image_filename]
            objects.append({'object_class': object_class, 'xmin': xmin, 'xmax': xmax, 'ymin': ymin, 'ymax': ymax})

        for image_filename, objects in image_objects.items():
            # Extract image dimensions
            img = Image.open(image_filename)
            image_width, image_height = img.size

            xml_tree = create_voc_xml(image_filename, objects, image_width, image_height)

            xml_filename = os.path.splitext(os.path.basename(image_filename))[0] + '.xml'
            output_path = os.path.join(output_dir, xml_filename)

            xml_tree.write(output_path)

# Usage
label_file = '../../test.csv'  # Replace with the path to your label file
output_dir = '../../xml_dir_train'  # Replace with the directory where you want to save the VOC XML files

convert_to_voc_xml(label_file, output_dir)
