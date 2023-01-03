import cv2
import numpy as np
from math import inf
from Search import Search

box_coordinates = []


def MSE(bloc_1, bloc_2):
    x, y = bloc_1.shape
    difference = np.square(bloc_1-bloc_2)
    return np.sum(difference)/(x*y)


def find_similar_bloc(image, searching_image, x, y, x2, y2) -> np.ndarray:

    width = y2-y
    height = x2-x

    BLOC_ENCADRE = image[y:y2, x:x2]

    dx, dy = 7, 7

    new_x, new_y = x-dx, y-dy
    new_w, new_l = x2+dx, y2+dy

    search_zone = searching_image[new_y:new_l, new_x:new_w]

    min_mse = inf
    min_bloc = None

    x_b2 = 0
    y_b2 = 0

    for x in range(search_zone.shape[0]):
        for y in range(search_zone.shape[1]):
            current_bloc = search_zone[y:y+width, x:x+height]
            if current_bloc.shape == BLOC_ENCADRE.shape:
                temp_mse = MSE(BLOC_ENCADRE, current_bloc)
                if min_mse > temp_mse:
                    min_mse = temp_mse
                    x_b2 = x
                    y_b2 = y
                    min_bloc = current_bloc
                    # cv2.imshow("bloc",current_bloc)
                    # cv2.waitKey(30)

    return search_zone, min_bloc, x_b2, y_b2, min_mse


def show_bloc(image, x, y, x2, y2, color=(255, 0, 0)):
    cv2.rectangle(image, (x, y, x2, y2), color, 2)
    while(True):
        cv2.imshow('image', image)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break


img1 = cv2.imread("./images/image072.png")
img2 = cv2.imread('./images/image092.png')

grayImg1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
grayImg2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)


image_1_YUV = grayImg1
image_2_YUV = grayImg2


def threshold_by_MSE(image1, image2, threshold=50):
    list_of_blocs = []
    x1, y1 = image1.shape
    bs = 16
    dx, dy = 7, 7

    for i in range(0, x1, bs):
        for j in range(0, y1, bs):
            _, _, x, y, min_mse = Search.sliding_search(
                image2, image1, i, j, i+bs, j+bs, dx, dy, bs)

            x_sz, y_sz = i-dx, j-dy

            x = x_sz+x
            y = y_sz+y

            if min_mse < threshold:
                list_of_blocs.append((x, y))

    for x, y in list_of_blocs:
        cv2.rectangle(img1, (y, x, bs, bs), (0, 0, 255), 2)

    cv2.imshow("image", img1)
    cv2.waitKey(10000)


threshold_by_MSE(image_1_YUV, image_2_YUV)
