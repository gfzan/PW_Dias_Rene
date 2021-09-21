import src.dataset.dsCOCO as ds
import os
import src.heatmap.hmCam as cam
import matplotlib.pyplot as plt
import numpy as np
import cv2

os.chdir('E:\GoogleDrive\FinalTask_IOL')

tupleArgs = ('E:/PROVA_VOC/ImgForClass_Test/cat/2010_003758.jpg', 'E:/MODEL/VGG16/camCOCO_20200731-140659_model.h5', ('global_average_pooling2d', 'dense'), 'conv2d')
prova = cam.HeatmapCam (*tupleArgs)

image, img_array = prova.image.img_for_cam(img_height=224, img_width=224)

heatmap = prova.cam_heatmap(img_array)

heatmapColored = prova.get_cam_for_img()

output = prova.overlay_heatmap()

# stampo le immagini
horizontal_concat_image = np.concatenate((image, heatmapColored, output), axis=1)

cv2.imshow('Immagini', horizontal_concat_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

(thresh, outputBbox) = prova.set_testBboxTxt(output)

outputGtBbox = prova.set_gtBboxTxt(output, 'E:\DATAset\VOCdevkit\VOC2012\Annotations')

# stampo le immagini
cv2.imshow('Immagine', output)
cv2.waitKey(0)
cv2.destroyAllWindows()

