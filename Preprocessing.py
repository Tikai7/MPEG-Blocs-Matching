import cv2
import numpy as np


class Preprocessing:

    @staticmethod
    def process_both(im1, im2, DELTA, padding=False):
        # grayImg1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        # grayImg2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
        yuvImg1 = cv2.cvtColor(im1, cv2.COLOR_RGB2YCrCb)
        yuvImg2 = cv2.cvtColor(im2, cv2.COLOR_RGB2YCrCb)

        luminance_image1 = np.expand_dims(yuvImg1[:, :, 0], axis=-1)
        luminance_image2 = np.expand_dims(yuvImg2[:, :, 0], axis=-1)

        luminance_image1 = luminance_image1.reshape(
            (luminance_image1.shape[0], luminance_image1.shape[1]))
        luminance_image2 = luminance_image2.reshape(
            (luminance_image2.shape[0], luminance_image2.shape[1]))

        # cv2.imshow("gray_image", luminance_image1)
        # cv2.waitKey(3000)

        if padding:
            luminance_image1 = Preprocessing.add_padding(
                luminance_image1, DELTA)

        return luminance_image1, luminance_image2

    @staticmethod
    def add_padding(image, DELTA=64):
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
