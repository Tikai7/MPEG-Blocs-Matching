import cv2
import time
import numpy as np
from Search import Search
from Preprocessing import Preprocessing
from tqdm import tqdm


class Find:
    @staticmethod
    def show_similarities(image, list_of_blocs, bs):
        for x, y in list_of_blocs:
            cv2.rectangle(image, (y, x, bs, bs), (0, 0, 255), 2)

        cv2.imshow("similarities_between_images", image)
        cv2.waitKey(15000)

    @staticmethod
    def show_residues(image2, list_of_blocs, bs):
        residue_image = np.copy(image2)
        for x, y in list_of_blocs:
            residue_image[x:x+bs, y:y+bs] = 0

        cv2.imshow("residues_between_images", residue_image)
        cv2.waitKey(15000)

    @staticmethod
    def with_sliding(im1, im2, threshold=50, dx=7, dy=7, bs=16, DELTA=64):

        print("[Preprocessing]...")
        image1, image2 = Preprocessing.process_both(im1, im2, DELTA)
        list_of_blocs = []
        x1, y1 = image1.shape

        print("[Searching]...")
        start = time.time()
        for i in tqdm(range(0, x1, bs)):
            for j in range(0, y1, bs):
                _, _, x, y, min_mse = Search.sliding_search(
                    image2, image1, i, j, i+bs, j+bs, dx, dy, bs, DELTA)

                x_sz, y_sz = i-dx, j-dy

                x = x_sz+x
                y = y_sz+y

                if min_mse < threshold:
                    list_of_blocs.append((x, y))
        end = time.time()

        print(f"[Result] in {end-start}s")
        print(f"[Preparing] image residues and similarities ...")

        Find.show_similarities(im1, list_of_blocs, bs)
        Find.show_residues(im2, list_of_blocs, bs)

        print(f"[Finish]")

    @staticmethod
    def with_dichotomic(im1, im2, threshold=50, bs=16, DELTA=64):

        print("[Preprocessing]...")
        image1, image2 = Preprocessing.process_both(im1, im2, DELTA)
        list_of_blocs = []
        x1, y1 = image1.shape

        print("[Searching]...")
        start = time.time()
        for i in tqdm(range(0, x1, bs)):
            for j in range(0, y1, bs):
                _, x, y, min_mse = Search.dichotomique_search(
                    image2, image1, i, j, i+bs, j+bs, bs, DELTA)
                if min_mse < threshold:
                    list_of_blocs.append((x, y))
        end = time.time()

        print(f"[Result] in {end-start}s")
        print(f"[Preparing] image residues and similarities ...")

        Find.show_similarities(im1, list_of_blocs, bs)
        Find.show_residues(im2, list_of_blocs, bs)

        print(f"[Finish]")
