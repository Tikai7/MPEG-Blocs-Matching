import numpy as np


class Error:
    @staticmethod
    def MSE(bloc_1, bloc_2) -> np.ndarray:
        x, y = bloc_1.shape
        difference = np.square(bloc_1-bloc_2)
        return np.sum(difference)/(x*y)
