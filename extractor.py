import numpy as np


class Extractor:
    def __init__(self, marked_ares):
        self.marked_ares = marked_ares

    def extruct_centers(self, indent=0):
        array_flat = self.marked_ares.flatten()
        array_flat_sorted_indices = array_flat.argsort()
        array_sorted_flat = array_flat[array_flat_sorted_indices]
        (unique,
         first,
         count) = np.unique(
            array_sorted_flat,
            return_index=True,
            return_counts=True
        )

        y, x = np.indices(self.marked_ares.shape)
        x = x.flatten()[array_flat_sorted_indices]
        y = y.flatten()[array_flat_sorted_indices]

        centers = np.zeros((len(unique)-indent, 2))

        for i in range(indent, len(unique)):
            x_shape = x[first[i]:first[i] + count[i]]
            y_shape = y[first[i]:first[i] + count[i]]
            x_center = np.mean(x_shape)
            y_center = np.mean(y_shape)
            center = np.array((x_center, y_center))
            centers[i-indent] = center

        return unique[indent:], centers

    def extruct_areas(self):
        unique, counts = np.unique(self.marked_ares, return_counts=True)
        return counts[2:-1]

    def extruct(self):
        return self.extruct_areas()

