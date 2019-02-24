#!/usr/bin/env python3

# Image Resizer
# Nathan Craddock
# 2019

try:
	from PIL import Image
except:
	print("PIL not installed... Aborting")
	sys.exit()
import os
import shutil
import sys
import argparse


# Array of possible output sizes
sizes = [(8192, 8192), (4096, 4096), (2048, 2048), (1024, 1024)]
size_map = {8192:"8k", 4096:"4k", 2048:"2k", 1024:"1k"}
image_types = ["ALB", "AO", "DIF", "DIS", "NOR", "OPA", "ROU"]
formats = ['png', 'jpeg']

# Parse input
parser = argparse.ArgumentParser(description='Batch-resize a directory of image files')
parser.add_argument('directories', help='a list of directory paths of images to resize', nargs='+')
parser.add_argument('-s', help='list of space delimited suffixes to keep at end of output filenames')
args = parser.parse_args()

dirs = args.directories

suffixes = args.s
if suffixes:
	suffixes = suffixes.split(' ')


def remove_suffix():
	pass


def check_out_path(out_path):
	# Make sure out_path exists
	# If it does, remove all files inside
	if not os.path.exists(out_path):
		os.mkdir(out_path)
	else:
		shutil.rmtree(out_path)
		os.mkdir(out_path)


def resize_image(im, path, name, format, sizes):
	# Create a copy
	temp = im.copy()

	if format == "jpeg":
		temp = temp.convert(mode='RGB')

	for size in sizes:
		# Create size subfolder
		image_output = path + os.sep + format + os.sep + size_map[size[0]]
		if not os.path.exists(image_output):
			os.makedirs(image_output)
			
		temp.thumbnail(size)

		# Remove suffix, insert size, append suffix
		for s in image_types:
			if name.endswith(s):
				name_suffix = name.rstrip(s)
				name_suffix = name_suffix + size_map[size[0]] + '_' + s

		# Get path of output
		image_name = name_suffix + '.' + format
		out_path = os.path.join(image_output, image_name)

		print("Writing", out_path)

		if format == "jpeg":
			temp.save(out_path, format, quality=90)
		else:
			temp.save(out_path, format)


def resize_images(path, out_path):
	for image_name in os.listdir(path):
		image_path = os.path.join(path, image_name)
		image_name_base = os.path.splitext(image_name)[0]
		
		print("Resizing:", image_path)

		im = Image.open(image_path)

		for format in formats:
			resize_image(im, out_path, image_name_base, format, sizes)


for dir in dirs:
	print("Reading images from", dir)
	out_path = dir + "_resized"
	check_out_path(out_path)

	resize_images(dir, out_path)
