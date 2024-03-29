import os
import cv2
from lxml import etree
import xml.etree.cElementTree as ET

def generate(folder, img, objects, tl, br, savedir):
	image = cv2.imread(str(img))
	h,w,d = image.shape

	annotation = ET.Element('annotated')
	ET.SubElement(annotation,'folder').text = folder
	ET.SubElement(annotation,'filename').text = img.name
	ET.SubElement(annotation,'segmented').text = '0'
	size = ET.SubElement(annotation,'size')
	ET.SubElement(size, 'width').text = str(w)
	ET.SubElement(size, 'height').text = str(h)
	ET.SubElement(size, 'depth').text = str(d)
	for obj_name, topl, botr in zip(objects, tl, br):
		ob = ET.SubElement(annotation, 'object')
		ET.SubElement(ob, 'name').text = obj_name
		ET.SubElement(ob, 'pose').text = 'Unspecified' 
		ET.SubElement(ob, 'truncated').text = '0'
		ET.SubElement(ob, 'difficult').text = '0'
		bbox = ET.SubElement(ob, 'bndbox')
		ET.SubElement(bbox, 'xmin').text = str(topl[0])
		ET.SubElement(bbox, 'ymin').text = str(topl[1])
		ET.SubElement(bbox, 'xmax').text = str(botr[0])
		ET.SubElement(bbox, 'ymax').text = str(botr[1])

	xml_str = ET.tostring(annotation)
	root = etree.fromstring(xml_str)
	xml_str = etree.tostring(root, pretty_print = True)

	save_path = os.path.join(savedir, folder.split('/')[1],img.name.replace('png', 'xml')) #use image name
	with open(save_path, 'wb') as temp_xml:
		temp_xml.write(xml_str)

if __name__ == '__main__':
    img = [im for im in os.scandir('data') if '22b.png' in im.name][0]
    objects = ['Head', 'Hands', 'Feet','Core','Hips','Legs','Arms']
    tl = [(50,50), (100,100)]
    br = [(500,500), (1000, 1000)]
    savedir = 'annotated'
    generate(folder, img, objects, tl, br, savedir)
