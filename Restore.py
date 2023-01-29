import cv2
import random
import numpy as np
from tqdm import tqdm

TIME = 5000


class Restore:
    @staticmethod
    def extract_from(list, i, j):
        for x, y, k, l in list:
            if k == i and l == j:
                return x, y
        return i, j

    @staticmethod
    def show_predictions(image1, residue_image, list_of_blocs, bs, mode):
        filename = "./out/predicted_image"
        predicted_image = residue_image.copy()

        for x, y, i, j in tqdm(list_of_blocs):
            zone_one = predicted_image[i:i+bs, j:j+bs]
            zone_two = image1[x:x+bs, y:y+bs]
            if zone_one.shape == zone_two.shape:
                predicted_image[i:i+bs, j:j + bs] = image1[x:x+bs, y:y+bs]
            else:
                bs_i = zone_two.shape[0]
                bs_j = zone_two.shape[1]
                predicted_image[i:i+bs_i, j:j +
                                bs_j] = image1[x:x+bs, y:y+bs]

        cv2.imwrite(f"{filename}.{mode}.jpg", predicted_image)
        cv2.imshow("predicted_image", predicted_image)
        cv2.waitKey(TIME)

    @staticmethod
    def show_similarities(image, image2, list_of_blocs, bs, mode):
        filename = "./out/similarities_image"
        for x, y, i, j in tqdm(list_of_blocs):
            # random_color = (random.randint(0, 255), random.randint(
            #     0, 255), random.randint(0, 255))

            color_one = (0, 0, 255)
            color_two = (255, 0, 0)

            cv2.rectangle(image, (y, x, bs, bs), color_one, 2)
            cv2.rectangle(image2, (j, i, bs, bs), color_two, 2)

        cv2.imwrite(f"{filename}_1.{mode}.jpg", image)
        cv2.imwrite(f"{filename}_2.{mode}.jpg", image2)

        cv2.imshow("similarities_between_images_1_2", image)
        cv2.imshow("similarities_between_images_2_1", image2)

        cv2.waitKey(TIME)
        return image

    @staticmethod
    def show_residues(image2, image1, list_of_blocs, list_of_residu, bs, mode):
        filename = "./out/residues_image"
        residue_image = np.copy(image2)

        for _, _, x, y in tqdm(list_of_blocs):
            residue_image[x:x+bs, y:y+bs] = 0

        working_residue = residue_image.copy()

        for _, _, x, y in tqdm(list_of_residu):
            residue_image[x:x+bs, y:y+bs] = abs(image1[x:x +
                                                       bs, y:y+bs]-image2[x:x+bs, y:y+bs])

        cv2.imwrite(f"{filename}.{mode}.jpg", residue_image)
        cv2.imshow("residues_between_images", residue_image)
        cv2.waitKey(TIME)
        return residue_image, working_residue
