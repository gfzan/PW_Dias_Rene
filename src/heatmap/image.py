from src.utils import *
import cv2
import numpy as np


class Image:

    def __init__(self, img_path):
        self.__image = cv2.imread(img_path)

    def get_image_copy(self) -> object:
        image_copy = self.__image
        return image_copy

    def img_for_cam(self, img_height=None, img_width=None):
        image = self.get_image_copy()
        print_likearray_info(image, 'image')
        img = cv2.resize(image, (img_height, img_width))  # scalo su valori per CNN
        img = np.expand_dims(img, axis=0)  # aggiungo dimensione del batch
        img_array = img / 255.  # applico trasformazione valori
        print_likearray_info(img_array, 'img_array')

        # ritorno il tensore img_array per il metodo gradcam_heatmap
        return image, img_array
