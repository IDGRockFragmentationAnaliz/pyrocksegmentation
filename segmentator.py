import numpy as np


class RockImageSegmentator:
	def __init__(self, image=None, edges_weighted=None):
		self.image = image
		self.edges_weighted = edges_weighted

	def get_background(self):
		result = np.uint8((self.edges_weighted / self.edges_weighted.max()) * 255)
		ret, background = cv2.threshold(result, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		return background

	def run(self):
		pass
