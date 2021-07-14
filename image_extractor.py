import os
import sys
import syglass as sy
from syglass import pyglass
import numpy as np
import tifffile
import subprocess

def extract(projectPath): 
	project = sy.get_project(projectPath)
	head, tail = os.path.split(projectPath)
	# Get a dictionary showing the number of blocks in each level
	#codebreak()
	resolution_map = project.get_resolution_map()

	# Calculate the index of the highest resolution level
	max_resolution_level = len(resolution_map) - 1

	# Determine the number of blocks in this level
	block_count = resolution_map[max_resolution_level]
	
	# get size of project       
	total_size = project.get_size(max_resolution_level)
	
	xsize = total_size[1]
	ysize = total_size[2]
	
	zslices = total_size[0]
	
	dimensions = np.asarray([1,xsize, ysize])
	offset = np.asarray([0,0,0])
	os.chdir(os.path.dirname(projectPath))
	for slice in range(zslices):
		s = str(slice).zfill(5)
		offset[0] = slice
		block = project.get_custom_block(0, max_resolution_level, offset, dimensions)
		data = block.data
		print(s + ".tiff")
		tifffile.imwrite(tail + "_" + s + ".tiff", data)
	subprocess.run(['explorer', head])

def main():
	print("Image Extractor, by Michael Morehead")
	print("Attempts to extract the original data volume from a syGlass project")
	print("and write it to a series of TIFF files")
	print("---------------------------------------")
	print("Usage: Highlight a project and use the Script Launcher in syGlass.")
	print("---------------------------------------")

	print(sys.argv)
	for syGlassProjectPath in sys.argv:
		print("Extracting project from: " + syGlassProjectPath)
		extract(syGlassProjectPath)

if __name__== "__main__":
	main()