import os
import numpy as np
import tifffile
import subprocess
import syglass as sy
import sys
import code


def extract(project): 
	projectPath = project.get_path_to_syg_file().string()
	print("Extracting project from: " + projectPath)
	head, tail = os.path.split(projectPath)
	# Get a dictionary showing the number of blocks in each level
	#codebreak()
	resolution_map = project.get_resolution_map()

	# Calculate the index of the highest resolution level
	max_resolution_level = len(resolution_map) - 1
	
	# get size of project       
	total_size = project.get_size(max_resolution_level)
	
	xsize = total_size[1]
	ysize = total_size[2]
	
	zslices = total_size[0]

	# get number of timepoints
	number_of_timepoints = project.get_timepoint_count()
	
	dimensions = np.asarray([1,xsize, ysize])
	offset = np.asarray([0,0,0])
	os.chdir(os.path.dirname(projectPath))
	for time in range(number_of_timepoints):
		zarray = []
		t = str(time).zfill(5)
		for slice in range(zslices):
			s = str(slice).zfill(5)
			offset[0] = slice
			block = project.get_custom_block(time, max_resolution_level, offset, dimensions)
			data = block.data
			channels = np.shape(data)[3]
			time = len(np.shape(data))
			file_name = head + "/" + tail[:-4] + "_Z-" + s + "_T-" + t + ".tiff"
			#code.interact(local=locals())
			if channels == 2:
				data = np.swapaxes(data, 1, 3)
				data = np.swapaxes(data, 2, 3)
				print("Writing " + file_name + "...")
				tifffile.imwrite(file_name, data, imagej=True, metadata={'axes': 'ZCYX'})
			elif time == 4:
				data = np.swapaxes(data, 1, 3)
				data = np.swapaxes(data, 2, 3)
				zarray.append(data)
			else:
				tifffile.imwrite(file_name, data)
		if len(zarray) > 0:
			#code.interact(local=locals())
			file_name = head + "/" + tail[:-4] + "_T-" + t + ".tiff"
			zstack = np.dstack(zarray)
			zstack = np.swapaxes(zstack, 0, 1)
			print("Writing " + file_name + "...")
			tifffile.imwrite(file_name, zstack, imagej=True, metadata={'axes': 'ZCYX'}) 
	head = head.replace("/", "\\")
	subprocess.Popen(f'explorer {head}')


def print_info():
	print("Image Extractor, by Michael Morehead")
	print("Attempts to extract the original data volume from a syGlass project")
	print("and write it to a series of TIFF files")
	print("---------------------------------------")
	print("Usage from CLI: image_extractor.py [path/to/project.syg]")
	print("---------------------------------------")
	print("Usage from syGlass: highlight projects from which to extract data")
	print("---------------------------------------")


def main(args):
	print_info()
	for project in args["selected_projects"]:
		extract(project)


if __name__ == "__main__":
	if not len(sys.argv) == 2:
		print_info()
	else:
		project_path = sys.argv[1]
		if not sy.is_project(project_path):
			print("Path provided does not describe a valid syGlass project")
		else:
			extract(sy.get_project(project_path))
