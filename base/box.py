import cv2
import numpy as np
from math import inf
import matplotlib.pyplot as plt

box_coordinates = []


def MSE(bloc_1,bloc_2):
    x,y = bloc_1.shape
    difference = np.square(bloc_1-bloc_2)
    return np.sum(difference)/(x*y)

def find_teach(image,searching_image)->np.ndarray:
    x,y = box_coordinates[0][0],box_coordinates[0][1]
    x2,y2 = box_coordinates[1][0],box_coordinates[1][1]

    width = y2-y
    height = x2-x

    BLOC_ENCADRE = image[y:y2,x:x2]

    dx,dy = 100,100

    new_x, new_y = x-dx,y-dy
    new_w, new_l = x2+dx,y2+dy

    search_zone = searching_image[new_y:new_l,new_x:new_w]
  
    min_mse = inf
    min_bloc = None

    x_b2 = 0
    y_b2 = 0

    for x in range(search_zone.shape[0]):
        for y in range(search_zone.shape[1]):
            current_bloc = search_zone[y:y+width,x:x+height]
            if current_bloc.shape == BLOC_ENCADRE.shape:
                temp_mse = MSE(BLOC_ENCADRE,current_bloc)
                if min_mse > temp_mse:
                    min_mse = temp_mse
                    x_b2 = x
                    y_b2 = y
                    min_bloc = current_bloc

    
    return search_zone,min_bloc,x_b2,y_b2


def show_bloc(image,x,y,x2,y2,color=(255,0,0)):
    cv2.rectangle(image, (x,y,x2,y2), color, 2)
    while(True):
        cv2.imshow('image', image)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break    

# mouse callback function
def draw_rect(event, x, y, flags, param):
    global box_coordinates 
    if event == cv2.EVENT_LBUTTONDOWN:
        box_coordinates=[(x, y)] 
      
    elif event == cv2.EVENT_LBUTTONUP:
        box_coordinates.append((x, y)) 
        cv2.rectangle(img, (box_coordinates[0][0], box_coordinates[0][1]), 
        (box_coordinates[1][0], box_coordinates[1][1]), (0, 0, 255), 2)
        cv2.imshow("image", img) 
            
	
img = cv2.imread("image072.png")
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_rect)

while(True):
	cv2.imshow('image', img)
	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		break
    
print(box_coordinates)
cv2.destroyAllWindows()

img1 = cv2.imread('image072.png')
grayImg1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
# Cropping an image
bloc1 = grayImg1[box_coordinates[0][1]:box_coordinates[1][1], box_coordinates[0][0]:box_coordinates[1][0]] 
# Display cropped image
cv2.imshow("cropped", bloc1)
cv2.waitKey(0)

img2 = cv2.imread("image092.png")
grayImg2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

search_zone,bloc,x_b2,y_b2 = find_teach(grayImg1,grayImg2)
bloc = bloc.astype(int)

x_b1,y_b1 = box_coordinates[0][0],box_coordinates[0][1]
x2_b1,y2_b1 = box_coordinates[1][0],box_coordinates[1][1]

bloc_width = y2_b1-y_b1
bloc_height = x2_b1-x_b1 

x_b2 = search_zone.shape[0] - x_b2
y_b2 = search_zone.shape[1] + y_b2

show_bloc(img1,x_b1,y_b1,bloc_height,bloc_width)
show_bloc(img2,x_b2,y_b2,bloc_height,bloc_width,color=(0,255,0))

            