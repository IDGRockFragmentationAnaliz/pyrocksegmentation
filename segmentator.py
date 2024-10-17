import cv2
import numpy as np
import scipy.ndimage.filters as filters
from matplotlib import pyplot as plt


class Segmentator:
	def __init__(self, image=None, edges_weighted=None, edges=None):
		self.image = image
		self.edges = edges
		self.edges_weighted = edges_weighted
		self.area_marks = None
		self.background = None

	def get_edges(self):
		if self.edges is not None:
			return self.edges

		result = np.uint8((self.edges_weighted / self.edges_weighted.max()) * 255)
		_, self.edges = cv2.threshold(result, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		return self.edges

	def get_background(self):
		if self.background is not None:
			return self.background
		self.background = 255 - self.get_edges()
		return self.background

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

	def remove_tiny_edges(self, threshold=500):
		edges = self.get_edges()
		_, edges_connected = cv2.connectedComponents(edges)
		num_edge, area_edge = np.unique(edges_connected, return_counts=True)
		edge_to_clean = {0: 0}
		for num_edge, area_edge in zip(num_edge[1:], area_edge[1:]):
			if area_edge < threshold:
				edge_to_clean[num_edge] = 0
			else:
				edge_to_clean[num_edge] = 255
		self.edges = (np.vectorize(lambda x: edge_to_clean[x])(edges_connected)).astype(np.uint8)
		print(self.edges)

	def run(self):
		kernel = np.ones((10, 10), np.uint8)
		self.edges = cv2.dilate(self.get_edges(), kernel, iterations=1)
		self.remove_tiny_edges()
		self.background = self.get_background()

		dt = cv2.distanceTransform(self.background, cv2.DIST_L2, 5)
		data_max = filters.maximum_filter(dt, 100)
		maxima = ((dt == data_max)*255).astype(np.uint8)
		maxima = cv2.dilate(maxima, kernel, iterations=1)
		self.area_marks = self.closes2segment(maxima)

		#return maxima + self.edges
		#self.area_marks = self.closes2segment(self.background)
		self.area_marks[self.area_marks == -1] = 0
		self.area_marks[self.area_marks == 1] = 0
		self.area_marks[self.edges == 255] = 1
		self.area_marks = cv2.watershed(self.image, self.area_marks)
		self.area_marks[self.area_marks == -1] = 0
		self.area_marks[self.area_marks == 1] = 0
		self.area_marks[self.edges == 255] = 1
		self.area_marks = cv2.watershed(self.image, self.area_marks)
		self.area_marks[self.area_marks == -1] = 0
		self.area_marks[self.area_marks == 1] = 0
		self.area_marks[self.edges == 255] = 1
		self.area_marks = cv2.watershed(self.image*0, self.area_marks)
		return self.area_marks + self.edges



