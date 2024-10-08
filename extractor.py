import numpy as np


class Extractor:
	def __init__(self, marked_ares):
		self.marked_ares = marked_ares

	def extruct_areas(self):
		unique, counts = np.unique(self.marked_ares, return_counts=True)
		return counts[2:-1]

	def extruct(self):
		return self.extruct_areas()

