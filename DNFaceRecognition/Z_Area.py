from PIL import Image, ImageDraw, ImageFile
import numpy as np
import random
import matplotlib.pyplot as plt



class Z_Area:
	def __init__(self, numNeurons):
		self.numNerons = numNeurons
		self.response = np.zeros(numNeurons)
		self.Y = []
		self.sampleY = np.zeros(numNeurons)



	def setY(self, Y):
		self.Y = Y



	def calculatePreResponse(self, YResponse):
		if not len(self.Y) :
			return False

		else:
			self.Y = YResponse
			return True

	def update(self):
		winner = self.Y[0]
		index = 0

		for i in range(1, self.numNerons):
			if self.Y[i] > winner:
				winner = self.Y[i]
				index = i
		return winner, index


