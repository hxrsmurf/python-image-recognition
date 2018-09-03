from PIL import Image
import StringIO
import urllib
import urlparse

import argparse
import io

import os
import shutil

src_dir = ""
dest_dir = ""
src_files = os.listdir(src_dir)

from google.cloud import vision
from google.cloud.vision import types
client = vision.ImageAnnotatorClient()

for a in src_files:
	dest_file = os.path.join(src_dir, a)
	#print "The file: " + dest_file
	with io.open(dest_file, 'rb') as image_file:
		resize_image = Image.open(image_file)
		resize_image.thumbnail((1024,768))
		buffer = StringIO.StringIO()
		resize_image.save(buffer, "PNG")
		content = buffer.getvalue()
		#content = image_file.read()
		image = types.Image(content=content)
		response = client.web_detection(image=image)
		image_path=response.web_detection.web_entities[0].description
		folder_path= dest_dir + image_path
		if not os.path.exists(folder_path):
			os.makedirs(folder_path)

		folder_path = folder_path + "/"
		full_filename = folder_path + a
		src_filename = src_dir + a

		shutil.move(src_filename, full_filename)
		print full_filename