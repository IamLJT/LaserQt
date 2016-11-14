from PIL import Image, ImageDraw, ImageFile
import numpy as np
import random
import matplotlib.pyplot as plt


class Y_Area:


	def __init__(self, numNeurons, xSize, zSize):
		self.numNeurons = numNeurons
		self.xSize = xSize
		self.zSize = zSize
		self.neuronalAges = np.ones(numNeurons)
		self.response = np.zeros(zSize)
		self.xNeurons = self.initNeurons(xSize, 'X')

		self.zNeurons = self.initNeurons(zSize, 'Z')
		# print(self.zNeurons)
		# np.zeros((numNeurons,zSize))#[np.zeros((zSize,1)) for z in range(numNeurons) ] #
		self.neuronalMatch = 0
		self.tmpX = np.zeros(xSize)
		self.tmpZ = np.zeros(zSize)

	def initNeurons(self, size, flag):
		# print('.ranNumber()', ranNumber)
		neurons = np.zeros((self.numNeurons,size))
		for i in range(self.numNeurons):
			for j in range(size):
				neurons[i][j] = random.randint(0, 256) if flag =='X' else random.uniform(0, 1)
			neurons[i] = neurons[i] /np.linalg.norm(neurons[i])
		# print(neurons[2])
		# print(neurons[3])
		return neurons
	
	def initTest(self, xNeruons, zNeruons):
		self.xNeruons = xNeruons
		self.zNeruons = zNeruons




	def calculatePreResponse(self, X, Z):
		winner = 0.0
		# self.tmpX = X
		# self.tmpZ = Z
		for n in range(0, self.numNeurons):

			bottomUpResponse = self.xNeurons[n].dot(X)
			topDownResponse = self.zNeurons[n].dot(Z)

			preResponse = bottomUpResponse +topDownResponse
			# print('topDownResponse')
			# print(topDownResponse)
			if preResponse > winner:
				winner = preResponse
				self.neuronalMatch = n
		# print('winner', winner)
		# print('neuronal Match ', self.neuronalMatch)

	def update(self, X,Z,isFrozen):
		
		zWeights = self.zNeurons[self.neuronalMatch]
		# print('Z is')
		# print(Z)
		if not isFrozen :
			# print(self.neuronalMatch)
			
			xWeights = self.xNeurons[self.neuronalMatch]
			# print(zWeights)
			age = self.neuronalAges[self.neuronalMatch] +1
			self.neuronalAges[self.neuronalMatch] = age
			w1 = (age -1.0)/age
			w2 = 1.0/age

			xWeights = w1* xWeights + w2* np.transpose(X)
			zWeights = w1* zWeights + w2* np.transpose(Z)
			# print(Z)
			# print(np.transpose(Z).shape)
			xWeights = xWeights /np.linalg.norm(xWeights)
			zWeights = zWeights /np.linalg.norm(zWeights)
			# print(zWeights)

			self.zNeurons[self.neuronalMatch] = zWeights
			self.xNeurons[self.neuronalMatch] = xWeights

		self.response = zWeights

	def saveNeuronAges(self):
		n = int(np.sqrt(self.numNeurons))
		plt.plot(self.neuronalAges)
		plt.ylabel('Age')
		plt.xlabel('Neuron')
		# plt.axis([0, 6, 0, 20])
		plt.savefig('plot_stem-ay.png')
		# plt.show()
		plt.close()


		with open('stem-ay.txt', 'w') as ay:
			ay.write(str(self.neuronalAges.reshape((n,n))))

		with open('stem-az.txt', 'w') as ay:
			ay.write(str(self.zNeurons[24]))
		plt.plot(self.zNeurons[24])
		plt.ylabel('Age')
		plt.xlabel('Neuron')
		# plt.axis([0, 6, 0, 20])
		plt.savefig('plot_stem-az.png')
		# plt.show()
		plt.close()

	def saveStemXY(self):
		n = int(np.sqrt(self.numNeurons))
		# print(self.xNeurons.shape)
		# stemXY = [[[] for x in range(n)] for y in range(n)] 
		stemXY = []
		whiteColumn= np.zeros((88,1))+255
		whiteRow = np.zeros((1,65))+255

		tmp = []

		for i in range(n):
			tmp = []
			for j in range(n):

				tmp1 = np.append(self.scale255(self.xNeurons[i*n+j]).reshape(88,64), whiteColumn, 1)
				tmp1 = np.append(tmp1, whiteRow, 0)

				# print('tmp1 shape ',tmp1.shape)
				if not len(tmp) :
					tmp = tmp1
				else:
					tmp = np.append(tmp, tmp1,1)
				# print('tmp shape ',tmp.shape)
			# print(tmp.shape)
			if not len(stemXY) :
					stemXY = tmp
			else:
					stemXY = np.append(stemXY, tmp,0)
			# stemXY = np.append(stemXY, tmp, 0)
			# print(stemXY.shape)

		stemXY= np.asarray(stemXY)
		# print(stemXY.shape)
		im =Image.fromarray(np.asarray(stemXY)).convert('L')
		im.show()
		im.save('stem-xy.pgm')

	def saveStemYZ(self):
		n = int(np.sqrt(self.numNeurons))
		# print(self.zNeurons)
		stemYZ = []
		whiteColumn= np.zeros((5,1))+255
		whiteRow = np.zeros((1,6))+255
		nerons = np.append(self.zNeurons, np.zeros((self.numNeurons,4)),1)

		for i in range(n):
			tmp = []
			for j in range(n):
				neurons = self.scale255(self.zNeurons[i*n+j]).reshape((1,self.zSize))
				neurons = np.append(neurons, np.zeros((1,4)),1)
				tmp1 = np.append(neurons.reshape((5,5)), whiteColumn, 1)
				tmp1 = np.append(tmp1, whiteRow, 0)

				if not len(tmp) :
					tmp = tmp1
				else:
					tmp = np.append(tmp, tmp1,1)

			if not len(stemYZ) :
					stemYZ = tmp
			else:
					stemYZ = np.append(stemYZ, tmp,0)


		stemYZ= np.asarray(stemYZ)
		# print(stemYZ.shape)
		im =Image.fromarray(np.asarray(stemYZ)).convert('L')
		im.show()
		im.save('stem-yz.pgm')

	def saveNetwork(self, fileName):
		print('x')


	def scale255(self, array):
		# array = np.nan_to_num(array)
		# if max(array) == min(array):
		# 	return array
		# else:
		return 255 * (array - min(array)) / (max(array) - min(array))















		
		





if __name__ == "__main__":
	print('main')
