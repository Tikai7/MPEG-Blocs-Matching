import numpy as np
from Error import Error
from math import inf


class Search:

    @staticmethod
    def dichotomique_search(target_bloc, searching_image, x, y, BS=16, DELTA=64) -> np.ndarray:

        step = 32
        min_mse = inf

        coord_x = x+DELTA
        coord_y = y+DELTA

        min_x = coord_x
        min_y = coord_y

        min_bloc = None

        while step >= 1:
            MOUVEMENTS = [(0, 0), (step, 0), (-step, 0), (0, step), (-step, 0),
                          (step, step), (-step, -step), (step, -step), (-step, step)]

            for move in MOUVEMENTS:
                n, m = move
                coord_x += n
                coord_y += m
                current_bloc = searching_image[coord_x:coord_x +
                                               BS, coord_y:coord_y+BS]
                if target_bloc.shape == current_bloc.shape:
                    temp_mse = Error.MSE(target_bloc, current_bloc)
                    if temp_mse < min_mse:
                        min_mse = temp_mse
                        min_x = coord_x
                        min_y = coord_y
                        min_bloc = current_bloc

                coord_x -= n
                coord_y -= m

            step //= 2

        return min_bloc, min_x, min_y, min_mse

    @staticmethod
    def sliding_search(target_bloc, searching_image, x, y, x2, y2, dx=7, dy=7, BS=16, DELTA=64) -> np.ndarray:

        WIDTH, HEIGHT = BS, BS
        DX, DY = dx, dy

        new_x, new_y = x-DX, y-DY
        new_x2, new_y2 = x2+DX, y2+DY

        search_zone = searching_image[new_x +
                                      DELTA:new_x2+DELTA, new_y+DELTA:new_y2+DELTA]

        min_mse = inf
        min_bloc = None

        x_b2 = 0
        y_b2 = 0

        for n in range(search_zone.shape[0]):
            for m in range(search_zone.shape[1]):
                current_bloc = search_zone[n:n+HEIGHT, m:m+WIDTH]
                if current_bloc.shape == target_bloc.shape:
                    temp_mse = Error.MSE(target_bloc, current_bloc)
                    if min_mse > temp_mse:
                        min_mse = temp_mse
                        x_b2 = n
                        y_b2 = m
                        min_bloc = current_bloc

        return search_zone, min_bloc, x_b2, y_b2, min_mse
