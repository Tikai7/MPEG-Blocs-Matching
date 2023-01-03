import cv2
from Find import Find

img1 = cv2.imread("./images/image072.png")
img2 = cv2.imread('./images/image092.png')

choice = input("\nType de recherche ?\n -1)Lineaire\n -2)Logarithmique\n")

algorithm = {
    '1': Find.with_sliding,
    '2': Find.with_dichotomic,
}

algorithm[choice](img1, img2, 50)
