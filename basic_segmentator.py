import cv2
import numpy as np
import scipy.ndimage.filters as filters
from matplotlib import pyplot as plt


class Segmentator:
	def __init__(self, edges):
		self.edges = edges
		self.area_marks = None
		self.background = None

	def get_edges(self):
		return self.edges

	def get_background(self):
		if self.background is not None:
			return self.background
		self.background = 255 - self.get_edges()
		return self.background

	def closes2segment(self, background=None):
		if background is None:
			background = self.get_background()
		print(background)
		_, area_marks = cv2.connectedComponents(background)
		self.area_marks = area_marks + 1
		return self.area_marks

	def get_segment_image(self):
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
		self.area_marks = self.closes2segment()

		self.area_marks[self.area_marks == -1] = 0
		self.area_marks[self.area_marks == 1] = 0
		img = np.zeros(self.area_marks.shape, np.uint8)
		img = cv2.merge((img, img, img))
		self.area_marks = cv2.watershed(img, self.area_marks)
		return self.area_marks
