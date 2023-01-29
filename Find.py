import time

from Search import Search
from Restore import Restore
from Preprocessing import Preprocessing
from tqdm import tqdm


class Find:

    @staticmethod
    def with_sliding(im1, im2, threshold=50, dx=7, dy=7, bs=16, DELTA=64):

        print("[Preprocessing]...")
        image1, image2 = Preprocessing.process_both(
            im1, im2, DELTA, padding=True)
        list_of_blocs = []
        list_of_residu = []

        x1, y1 = image2.shape

        print("[Searching]...")
        start = time.time()
        for i in tqdm(range(0, x1, bs)):
            for j in range(0, y1, bs):
                target_bloc = image2[i:i+bs, j:j+bs]
                if target_bloc.shape == (bs, bs):
                    _, _, x, y, min_mse = Search.sliding_search(
                        target_bloc, image1, i, j, i+bs, j+bs, dx, dy, bs, DELTA)

                    x_sz, y_sz = i-dx, j-dy

                    x = x_sz+x
                    y = y_sz+y

                    if min_mse < threshold:
                        list_of_blocs.append((x, y, i, j))
                    else:
                        list_of_residu.append((x, y, i, j))

        end = time.time()

        print(f"[Result] in {end-start}s")

        print(f"[Preparing] image similarities ...")
        Restore.show_similarities(im1.copy(), list_of_blocs, bs, mode="lin")
        print(f"[Done]")

        print(f"[Preparing] image residues ...")
        residue_image = Restore.show_residues(
            im2, im1, list_of_blocs, list_of_residu, bs, mode="lin")
        print(f"[Done]")

        print(f"[Preparing] image predicted ...")
        Restore.show_predictions(im1, residue_image,
                                 list_of_blocs, bs, mode="lin")

        print(f"[Finish]")

    @staticmethod
    def with_dichotomic(im1, im2, threshold=50, bs=16, DELTA=64):

        print("[Preprocessing]...")
        image1, image2 = Preprocessing.process_both(
            im1, im2, DELTA, padding=True)
        list_of_blocs = []
        list_of_residu = []
        x1, y1 = image2.shape

        print("[Searching]...")
        start = time.time()
        for i in tqdm(range(0, x1, bs)):
            for j in range(0, y1, bs):
                target_bloc = image2[i:i+bs, j:j+bs]
                if target_bloc.shape == (bs, bs):
                    _, x, y, min_mse = Search.dichotomique_search(
                        target_bloc, image1, i, j, bs, DELTA)
                    if min_mse < threshold:
                        list_of_blocs.append((x-DELTA, y-DELTA, i, j))
                    else:
                        list_of_residu.append((x-DELTA, y-DELTA, i, j))

        end = time.time()

        print(f"[Result] in {end-start}s")

        print(f"[Preparing] image similarities ...")
        Restore.show_similarities(
            im1.copy(), im2.copy(), list_of_blocs, bs, mode="log")
        print(f"[Done]")

        print(f"[Preparing] image residues ...")
        residue_image = Restore.show_residues(
            im2, im1, list_of_blocs, list_of_residu, bs, mode="log")
        print(f"[Done]")

        print(f"[Preparing] image predicted ...")
        Restore.show_predictions(im1, residue_image,
                                 list_of_blocs, bs, mode="log")

        print(f"[Finish]")
