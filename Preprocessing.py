import cv2


class Preprocessing:

    @staticmethod
    def process_both(im1, im2, DELTA, padding=False):
        grayImg1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        grayImg2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

        if padding:
            grayImg1 = Preprocessing.add_padding(grayImg1, DELTA)

        return grayImg1, grayImg2

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
