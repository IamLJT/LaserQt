from PIL import Image, ImageDraw, ImageFile
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import os
np.set_printoptions(threshold=np.nan)
import matplotlib.pyplot as plt
import json
from Y_Area import Y_Area
from Z_Area import Z_Area
import json

EPSILON = 1e-12


import sys
import getopt
Image_Size = (64, 88)
CLASS_MAX = 128


def main(argv):
	inputFilenamelist = ''
	outputfile = ''
	networkfile = ''
	epoches = 0
	# False : train Ture test
	isTest = True
	numYNeurons = 0
	n = 0

	try:
		opts, args = getopt.getopt(
			argv, "hl:f:Y:d:o:", ["e=", "ifile=", "Yn=", "ofile="])
	except getopt.GetoptError:
		print('python3 dn.py -l e -f filenamelist -Y n -d databasefile -o outputfile')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(' python3 dn.py -l e -f filenamelist -d networkfile -o outputfilename')
			sys.exit()
		elif opt in ("-l", "--e"):
			isTest = False
			epoches = arg
		elif opt in ("-f", "--ifile"):
			inputFilenamelist = arg
		elif opt in ("-Y", "--Yn"):
			n = arg
		elif opt in ("-d", "--nfile"):
			networkfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
	# print('Input file is ', inputFilenamelist)
	# print('Output file is ', outputfile)
	# print('Epoches is ', epoches)
	numYNeurons = int(n) * int(n)
	# print('numYNeurons is ', numYNeurons)
	numClasses, fileList = readInputFileList(inputFilenamelist)

	if not isTest:
		print('Training phase')
		print('Total training files: ', len(fileList))
		zSize = int(numClasses)+ 1

		print('Total training classes: ', int(numClasses))
		X = np.zeros((Image_Size[0] * Image_Size[1], 1))
		Z = np.zeros((zSize,1))
		Y = Y_Area(numYNeurons, len(X), len(Z))
		currentClass = ''
		classIndex = 0

		#t =1
		bgImg, bgClass, bgName = getImageInfo(os.path.dirname(
						inputFilenamelist) + '/background1.raw')


		className = []
		# print(len(Z))
		with open(networkfile, "wb") as netFile:
			# numclasses
			netFile.write(str(numYNeurons).encode())
			netFile.write(b'|')
			netFile.write(str(zSize).encode())
			netFile.write(b'|')
			"""
			for epoch in range(0, int(epoches)):
				for f in range(0, len(fileList)):
					currentImage, currentImageClass, currentImageFileName = getImageInfo(os.path.dirname(
							inputFilenamelist) + '/' + fileList[f])

					X = currentImage

					if currentImageClass != currentClass and epoch == 0:
						Z = np.zeros((zSize,1))
						classIndex +=1
						Z[classIndex] = 1
						currentClass = currentImageClass
						className.append(currentClass)

					for i in range(0,2):
								Y.calculatePreResponse(X,Z)
								Y.update(X,Z, False)

			"""

			for epoch in range(0, int(epoches)):
				print('The '+ str(epoch+1)+' epoch')
				currentClass = bgClass
				Z = np.zeros((zSize,1))
				X = bgImg
				Z[0] = 1

				#t=1
				Y.calculatePreResponse(X,Z)
				Y.update(X,Z, False)
				oldX= X
				oldZ = Z

				#t=2
				classIndex = 0
				currentClass = bgClass
				Z = np.zeros((zSize,1))
				X = bgImg
				Z[0] = 1
				Y.calculatePreResponse(X,Z)
				Y.update(X,Z, False)
				oldX = X
				oldZ = Z


				#t=3
				for f in range(0, len(fileList)):
					# print(fileList[f])
					#compute the 
					if  f == 0:
						currentImage, currentImageClass, currentImageFileName = getImageInfo(os.path.dirname(
							inputFilenamelist) + '/' + fileList[f])
						currentClass = currentImageClass
						if epoch == 0:
							className.append(currentClass)
						Y.calculatePreResponse(oldX,oldZ)
						Y.update(oldX,oldZ, False)

						oldX = currentImage
						for i in range(0,2):
							Y.calculatePreResponse(oldX,oldZ)
							Y.update(oldX,oldZ, False)
						oldZ = np.zeros((zSize,1))
						classIndex +=1
						oldZ[classIndex] = 1

					else:
						
						currentImage, currentImageClass, currentImageFileName = getImageInfo(os.path.dirname(
								inputFilenamelist) + '/' + fileList[f])
						# X = currentImage
						# print(currentClass)


						if currentImageClass != currentClass :

							# X = currentImage
						# print(Z)
							Y.calculatePreResponse(oldX,oldZ)
							Y.update(oldX,oldZ, False)
							X = bgImg
							for i in range(0,2):
								Y.calculatePreResponse(X,oldZ)
								Y.update(X,oldZ, False)
							# for j in range(len(oldZ)):
							#     oldZ[j] = 0
							# oldZ[0] =1
							oldZ = np.zeros((zSize,1))
							oldZ[0] =1
							X = currentImage
							for i in range(0,2):
								Y.calculatePreResponse(X,oldZ)
								Y.update(X,oldZ, False)
							oldZ = np.zeros((zSize,1))
							classIndex +=1
							oldZ[classIndex] = 1
							currentClass = currentImageClass 
							if epoch == 0:
								className.append(currentClass)                   
							oldX = currentImage

						else:
							Y.calculatePreResponse(currentImage,oldZ)
							Y.update(currentImage,oldZ, False)
							oldX = currentImage
						
						# for i in range(0,2):
						#         Y.calculatePreResponse(X,oldZ)
						#         Y.update(X,oldZ, False)
						# oldX = X
			
			netFile.write(str(json.dumps(className)).encode())
			netFile.write(b'|')
			netFile.write(str(json.dumps(Y.xNeurons.tolist())).encode())
			netFile.write(b'|')
			netFile.write(str(json.dumps(Y.zNeurons.tolist())).encode())
			netFile.write(b'|')
			# print(Y.neuronalAges)
			Y.saveNeuronAges()
			Y.saveStemXY()
			Y.saveStemYZ()

	else:
		print('Testing phase')
		print('Total testing files: ', len(fileList))
		
		X = np.zeros((Image_Size[0] * Image_Size[1], 1))
		
		currentClass = ''
		classIndex = 0

		#t =1
		bgImg, bgClass, bgName = getImageInfo(os.path.dirname(
						inputFilenamelist) + '/background2.raw')
		with open(networkfile, "rb") as netFile:
			# numclasses
			data = netFile.read().decode().strip().split("|")
			# print(data)
			numNeurons =  int(data[0])

			zSize = int(data[1])

			xNeurons = np.array(json.loads(data[3]), dtype = float)
			zNeurons = np.array(json.loads(data[4]), dtype = float)
			# zSize = int(numClasses)
			className = json.loads(data[2])
			# print(len(className))

			Z = Z_Area(zSize)
			Y = Y_Area(numNeurons,len(X), zSize)
			Y.initTest(xNeurons,zNeurons)
			Z.setY(Y.response)

			correctNo = 0
			X = bgImg
			with open(outputfile, "w") as resultFile:
				resultFile.write('Input file name; the reported name from Z; the response value of the highest Z neuron.\n')
				for testFile in range(0, len(fileList)): 

					currentImage, currentImageClass, currentImageFileName = getImageInfo(os.path.dirname(
								inputFilenamelist) + '/' + fileList[testFile])

					for i in range(0, len(className)):
						if className[i] == currentImageClass:
							classIndex = i
							break
					# Z.setY(Y.response)
					Z.resopnse = np.zeros((zSize,1))
					# print(Z.response)
					# if testFile ==0:
					# 	Z.resopnse = np.zeros((zSize,1))
					# 	Z.resopnse[0] =1
					# else:
					# 	Z.resopnse = np.zeros((zSize,1))
					Y.calculatePreResponse(X, Z.response)

					Z.calculatePreResponse(Y.response)
					
					X = currentImage
					Y.update(X,Z.response, True)

					Z.setY(Y.response)
					responseValue, index = Z.update()

					# print('select index is ', str(index+1))
					if (index -1) == classIndex:
						correctNo +=1
					resultFile.write(currentImageFileName + ' ; '+ className[index-1]  + ' ; '+ str(responseValue)+'\n')
				print('The recognition rate {0:.2f}%'.format(100*correctNo/len(fileList)))
				resultFile.write('The recognition rate : {0:.2f}%'.format(100*correctNo/len(fileList)))

		


def readInputFileList(path):
	fileList = []
	
	with open(path) as f:
		numClasses = f.readline().strip()
		for line in f:
			if not line.strip().isdigit() and line.strip() != "":
				fileList.append(line.strip())
	return numClasses, fileList

def scale255(array):
	return 255 * (array - min(array)) / (max(array) - min(array))

def getImageInfo(filePath):
	fileName = os.path.split(filePath)[1]
	if fileName.split(".")[0][-2].isupper() or fileName.split(".")[0][-2].isdigit() :
		classLabel = fileName.split(".")[0][0:-2]
	else:
		classLabel = fileName.split(".")[0][0:-1]
	#print(fileName.split(".")[0][-2])
	
	#print(classLabel)
	f = open(filePath, "rb")
	fileContent = f.read()
	f.closed
	im = Image.frombytes("L", Image_Size, fileContent, decoder_name='raw')
	# im.show()
	pixels = np.array(im)
	#print(pixels)
	pixels = np.reshape(pixels, (64 * 88, 1))
	# print(pixels.shape)
	pixels = pixels/np.linalg.norm(pixels)
	return pixels, classLabel,fileName



def calculateAmnesic(t):
	t1 = 10
	t2 = 200
	r = 1000
	c = 2
	ut = 0
	if t <= t1:
		ut = 0
	elif t > t1 and t <= t2:
		ut = c * (t - t1) / (t2 - t1)
	else:
		ut = c + (t - t2) / r

	w1 = (t - 1 - ut) / t
	w2 = (1 + ut) / t
	return w1, w2


if __name__ == "__main__":
	 #getImageInfo("841Fall16/AdiMatthew10.raw")
	main(sys.argv[1:])
