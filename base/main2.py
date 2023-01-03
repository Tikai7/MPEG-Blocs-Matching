import cv2
import numpy as np

BS = 16
DELTA = 64


def add_padding(image, DELTA):
    image_with_padding = cv2.copyMakeBorder(
        image,
        DELTA,
        DELTA,
        DELTA,
        DELTA,
        cv2.BORDER_CONSTANT,
        None,
        0
    )
    return image_with_padding


def MSE(bloc_1, bloc_2):
    x, y = bloc_1.shape
    difference = np.square(bloc_1-bloc_2)
    return np.sum(difference)/(x*y)


def dichotomique_search(bloc, searching_image, x, y) -> np.ndarray:

    step = 32
    new_x = x+DELTA
    new_y = y-DELTA
    blocs_to_encode = []

    while step >= 1:
        compared_bloc = searching_image[new_x:new_x+BS, new_y:new_y+BS]
        mse = MSE(bloc, compared_bloc)

        step /= 2

    return coord_x, coord_y


def predictive_latent_space_translation(image1, image2):

    for x in range(0, image2.shape[0], BS):
        for y in range(0, image2.shape[1], BS):
            current_bloc = image2[x:x+BS, y:y+BS]
            coord_x, coord_y = dichotomique_search(current_bloc, image1, x, y)


def load_image(path):
    img = cv2.imread(path)
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


img1_gray = load_image('image072.png')
img1_gray = add_padding(img1_gray)

img2_gray = load_image('image092.png')


predictive_latent_space_translation(img1_gray, img2_gray)
