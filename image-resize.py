#!/usr/bin/env python3

# Image Resizer
# Nathan Craddock
# 2019

import sys

try:
	from PIL import Image
except:
	print("PIL not installed... Aborting")
	sys.exit()

import os
import shutil
import argparse
import zipfile


# Array of possible output sizes
sizes = [(8192, 8192), (4096, 4096), (2048, 2048), (1024, 1024)]
size_map = {8192:"8K", 4096:"4K", 2048:"2K", 1024:"1K"}
image_types = ["ALB", "AO", "DIF", "DIS", "NOR", "OPA", "ROU"]

# Parse input
parser = argparse.ArgumentParser(description='Batch-resize a directory of image files')
parser.add_argument('directories', help='a list of directory paths of images to resize', nargs='+')
parser.add_argument('-s', help='list of space delimited suffixes to keep at end of output filenames')
parser.add_argument('-f', help='comma-separated list of output formats [-f=jpeg,png,webp]')
args = parser.parse_args()

dirs = args.directories

suffixes = args.s
if suffixes:
	suffixes = suffixes.split(' ')

formats = args.f
if formats:
	l = formats.rstrip('=')
	formats = l.split(',')

	if 'jpg' in formats:
		formats[formats.index('jpg')] = 'jpeg'

	# Ensure no duplicate types
	formats = set(formats)
else:
	formats = ['jpeg', 'png']

basename = ""

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


def resize_image(im, in_path, path, name, format, sizes):
	# Create a copy
	temp = im.copy()

	if format == "jpeg":
		temp = temp.convert(mode='RGB')

	for size in sizes:
		# Create size subfolder
		if format == "jpeg":
			folder_output = path + os.sep + "JPG" + os.sep + basename + " " + size_map[size[0]]
		else:
			folder_output = path + os.sep + format.upper() + os.sep + basename + " " + size_map[size[0]]
		if not os.path.exists(folder_output):
			os.makedirs(folder_output)
		#print(folder_output)
			
		temp.thumbnail(size)

		name_suffix = name
		# Remove suffix, insert size, append suffix
		for s in image_types:
			if name.endswith(s):
				name_suffix = name.rstrip(s)
				name_suffix = name_suffix + size_map[size[0]] + '_' + s

		# Get path of output
		if format == "jpeg":
			image_name = name_suffix + '.jpg'
		else:
			image_name = name_suffix + '.' + format

		out_path = os.path.join(folder_output, image_name)

		print("Writing", out_path)

		if format == "jpeg":
			temp.save(out_path, format, quality=90)
		elif format == "webp":
			temp.save(out_path, format, quality=90)
		else:
			if size[0] == 8192:
				shutil.copy2(in_path, out_path)
			else:
				temp.save(out_path, format)

		# zip folder
		z = zipfile.ZipFile(folder_output + ".zip", 'a')
		for image in os.listdir(folder_output):
			z.write(os.path.join(folder_output, image), basename + " " + size_map[size[0]] + os.sep + image)
		z.close()

		# remove folder
		shutil.rmtree(folder_output)

	print()

def resize_images(path, out_path):
	for image_name in os.listdir(path):
		if os.path.isfile(os.path.join(path, image_name)):
			image_path = os.path.join(path, image_name)
			image_name_base = os.path.splitext(image_name)[0]

			print("Resizing:", image_path)

			im = Image.open(image_path)

			for format in formats:
				resize_image(im, image_path, out_path, image_name_base, format, sizes)


for dir in dirs:
	print("Reading images from", dir)
	out_path = dir + "_resized"
	check_out_path(out_path)

	basename = os.path.basename(dir)
	print("Basename:", basename)

	resize_images(dir, out_path)
