import os
import shutil

sourceFolder = ''
destinationFolder = ''

for path, subdirs, files in os.walk(sourceFolder):
	for name in files:
		fullPath = os.path.join(path,name)
		shutil.move(fullPath, destinationFolder)		