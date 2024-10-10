import cv2
import numpy as np
from matplotlib import pyplot as plt


class Segmentator:
	def __init__(self, image=None, edges_weighted=None):
		self.image = image
		self.edges_weighted = edges_weighted

	def get_background(self):
		result = np.uint8((self.edges_weighted / self.edges_weighted.max()) * 255)
		ret, background = cv2.threshold(result, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		return background

	def closes2segment(self, background=None):
		if background is None:
			background = self.background
		_, area_marks = cv2.connectedComponents(background)
		area_marks = area_marks + 1
		return area_marks

	def run(self):
		bg = self.get_background()
		area_marks = self.closes2segment(255 - bg)

		# fig = plt.figure(figsize=(14, 9))
		# axs = [fig.add_subplot(3, 1, 1),
		#        fig.add_subplot(3, 1, 2),
		#        fig.add_subplot(3, 1, 3)]
		# axs[0].imshow(self.edges_weighted)
		# axs[1].imshow(bg)
		# axs[2].imshow(area_marks)
		# plt.show()

		area_marks[area_marks == -1] = 0
		area_marks[area_marks == 1] = 0
		area_marks = cv2.watershed(self.image, area_marks)
		return area_marks



