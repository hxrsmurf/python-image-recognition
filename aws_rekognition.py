# AWS Rekognition - https://docs.aws.amazon.com/rekognition/latest/dg/what-is.html
# Poorly done by Kevin "hxrsmurf" Murphy
# 2018 September

import argparse
import boto3
import json
import os
import shutil
from PIL import Image

# Delete the thumbnail/scaled folder after done rekognizing. Manually implemented right now. 
def cleanupFolder():
	shutil.rmtree(thumbnailFolder)

# Move all of the images we just sorted and put them back in the root directory.
def resetImagesAndFolders():
	for path, subdirs, files in os.walk(resetSource):
		for name in files:
			fullPath = os.path.join(path,name)
			print('Moving ' + name)
			shutil.move(fullPath,resetSource)

# Create the staging folders, not used for celebrity
def createFolders():
	for folders in createFolders:
		newFolder = directory + folders
		if not os.path.exists(newFolder):
			os.makedirs(newFolder)
			print('Creating staging folder: ' + newFolder)

# This function is used to downscale the image. There isa 5 MB file size limit.
def createThumbnails():
	for fileName in os.listdir(directory):
		fullPath = (directory + fileName)
		completePath = (completeFolder + fileName)
		otherPath = (otherFolder + fileName)
		if os.path.isfile(fullPath):
			extension = os.path.splitext(fullPath)[-1].lower()
			if extension == '.jpg' or extension == '.jpeg' or extension == '.png':
				resizePhoto = Image.open(fullPath)
				size = (resizePhoto.width, resizePhoto.height)
				resizePhoto.thumbnail(size, Image.ANTIALIAS)
				if extension == '.jpg' or extension == '.jpeg':
					resizePhoto.save(thumbnailFolder + fileName, "JPEG")
				elif extension == '.png':
					resizePhoto.save(thumbnailFolder + fileName, "PNG")
				else:
					shutil.move(fullPath,otherPath)
				# Sometimes the thumbnail wouldn't create without this.	
				resizePhoto.close()			
				shutil.move(fullPath,completePath)
			else:
				resizePhoto.close()		
				shutil.move(fullPath,otherPath)
				
# AWS Image Rekognition by creating folders based on the celebrity's face and moving the image there
def rekognizeCelebrities():
	for fileName in os.listdir(celebrityFolder):
		fullPath = (celebrityFolder + fileName)
		# I wasn't sure how to do this better, but this works.
		if fileName == "Thumbs.db":
			pass
		else:			
			if os.path.isfile(fullPath):
				with open(fullPath, 'rb') as image:
					response = client.recognize_celebrities(Image={'Bytes': image.read()})
					if not response['CelebrityFaces']:
						pass
					else:					
						for celebrity in response['CelebrityFaces']:
							celebrity = celebrity['Name']
							labelFolder = celebrityFolder + celebrity
							celebrityPath = labelFolder + '\\' + fileName
							if not os.path.exists(labelFolder):
								os.makedirs(labelFolder)
								print(labelFolder)
						
							if celebrity:
								print('found ' + celebrity)
							else:
								# need to move the file to another folder.
								pass
							print('Moving ' + fullPath + ' to ' + celebrityPath)
							image.close()
							shutil.move(fullPath,celebrityPath)
							
# AWS Image Rekognition by creating folders based on the label and moving the image there. This is the main function. 
def rekognizeLabels():
	for fileName in os.listdir(thumbnailFolder):
		fullPath = (thumbnailFolder + fileName)
		
		with open(fullPath, 'rb') as image:
			#  I'd like to implement a selector so I can easily select what it should be. 
			response = client.detect_labels(Image={'Bytes': image.read()},MaxLabels=1)
			for label in response['Labels']:
				label = label['Name']
				labelFolder = completeFolder + label	
				if not os.path.exists(labelFolder):
					os.makedirs(labelFolder)
					print(labelFolder)
				fullPath = (completeFolder + fileName)
				labelPath = (labelFolder + '\\' + fileName)
				print('Moving ' + fullPath + ' to ' + labelPath)
				image.close()
				shutil.move(fullPath,labelPath)
				

# The main function to prep the directories for AWS Image Rekognition with Labels
def beginLabelRekognize():
	createFolders()
	createThumbnails()
	rekognizeLabels()

# Redundant so I can easily put my folders in. 
def nullDirectories():
	createFolders  = ''
	directory  = ''
	thumbnailFolder  = ''
	completeFolder  = ''
	otherFolder  = ''
	resetSource  = ''
	resetDestination  = ''
	celebrityFolder  = ''

# Directory configuration. Note: use two \\ on Windows. For example, "C:\\Windows\\"
celebrityFolder  = ''
client=boto3.client('rekognition')
completeFolder  = ''
createFolders  = ''
directory  = ''
otherFolder  = ''
resetDestination  = ''
resetSource  = ''
thumbnailFolder  = ''
	
def helloWorld():
	print('Hello World')

parser = argparse.ArgumentParser(description='Small Python script to use Amazon Web Services\' Rekognition to sort images by celebrity or by the first label it finds.')
parser.add_argument('-hw', action='store_true', help='Hello World')
parser.add_argument('-reset', action='store_true', help='Unorganize images - grab all images and put them in root directory')
parser.add_argument('-cleanup', action='store_true', help='Remove Thumbnail Folder')
parser.add_argument('-celebrities', action='store_true', help='Rekognize Celebrities')
parser.add_argument('-label', action='store_true', help='Rekognize Pictures by Label')
args = parser.parse_args()

if args.hw:
	helloWorld()
elif args.reset:
	resetImagesAndFolders()
elif args.cleanup:
	cleanupFolder
elif args.celebrities:
	rekognizeCelebrities
elif args.label:
	beginLabelRekognize
else:
	helloWorld()