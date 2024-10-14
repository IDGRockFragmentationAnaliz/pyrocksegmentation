import cv2
import numpy as np
from matplotlib import pyplot as plt


class Segmentator:
	def __init__(self, image=None, edges_weighted=None):
		self.image = image
		self.area_marks = None
		self.background = None
		self.edges_weighted = edges_weighted

	def get_background(self):
		result = np.uint8((self.edges_weighted / self.edges_weighted.max()) * 255)
		ret, background = cv2.threshold(result, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		return background

	def closes2segment(self, background=None):
		if background is None:
			background = self.background
		_, area_marks = cv2.connectedComponents(background)
		self.area_marks = area_marks + 1
		return self.area_marks

	def get_segment_image(self):
		print(1)
		values = np.unique(self.area_marks)
		red, green, blue = {}, {}, {}
		for value in values:
			red[value] = np.random.randint(0, 255)
			green[value] = np.random.randint(0, 255)
			blue[value] = np.random.randint(0, 255)
		fun = np.vectorize(lambda x: (red[x], green[x], blue[x]))
		return cv2.merge(fun(self.area_marks))


	def run(self):
		self.background = self.get_background()
		self.area_marks = self.closes2segment(255 - self.background)
		self.area_marks[self.area_marks == -1] = 0
		self.area_marks[self.area_marks == 1] = 0
		self.area_marks = cv2.watershed(self.image, self.area_marks)
		return self.area_marks



