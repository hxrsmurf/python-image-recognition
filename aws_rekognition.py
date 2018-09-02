import boto3
import json
import os
import shutil

client=boto3.client('rekognition')
imageFolder = ''
emptyFolder = imageFolder + 'unsorted'

if not os.path.exists(emptyFolder):
	os.makedirs(emptyFolder)

for fileName in os.listdir(imageFolder):
	photo = imageFolder + fileName
	if os.path.isdir(photo):
		pass
	else:
		extension = os.path.splitext(fileName)[-1]
		if not extension == '.jpg' or extension == '.png':
			pass
		else: 
			with open(photo, 'rb') as image:
				response = client.recognize_celebrities(Image={'Bytes': image.read()})
			if not response['CelebrityFaces']:	
				unsortedPhoto = emptyFolder + '\\' + fileName
				shutil.move(photo, unsortedPhoto)
				print('Not found, moving to unsorted')
			else:
				for celebrity in response['CelebrityFaces']:
					newFolder = imageFolder + celebrity['Name']
					if not os.path.exists(newFolder):
						os.makedirs(newFolder)
					newPhoto = newFolder + '\\' + fileName
					if photo:
						pass
					else:
						shutil.move(photo, newPhoto)
						print('Found! Moving to ' + celebrity['Name'])