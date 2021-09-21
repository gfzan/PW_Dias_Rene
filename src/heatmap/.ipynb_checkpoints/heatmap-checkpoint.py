from src.heatmap.image import Image
from src.heatmap.conv_net import ConvNet
from src.utils import *
import os
import xml.etree.ElementTree as ET

import cv2
import numpy as np


class Heatmap:

    def main(self):
        pass

    @classmethod
    def from_input(cls):
        return cls(
            img_path=input('\n inserire percorso immagine da testare : \n'),
            path_model=input("\n inserire percorso modello CNN addestrato e salvato : \n"),
            last_conv_layer_name=input("\n inserire nome dell'ultimo strato di convoluzione : \n"),
            classifier_layer_names=input("\n inserire nomi degli ''strati densi'' : \n")
        )

    # COSTRUTTORE
    def __init__(self, img_path, path_model, classifier_layer_names, last_conv_layer_name=None,
                 img_height=224, img_width=224):
        self.img_path = img_path
        self.path_model = path_model
        self.classifier_layer_names = classifier_layer_names
        self.last_conv_layer_name = last_conv_layer_name
        self.img_height = img_height
        self.img_width = img_width
        self.image = Image(self.img_path)                     # passo un oggetto di classe Image
        self.img_original = self.image.get_image_copy()   # creo una copia dell'istanza image
        self.conv_model = ConvNet(self.path_model, self.classifier_layer_names, self.last_conv_layer_name)

        self.heatmap = []
        self.heatmapResizeImg = []
        self.heatmapResizeImg1ch = []

    def get_cam_for_img(self):
        # heatmap riscalata in dimensioni e valori
        heatmap_resize = cv2.resize(self.heatmap, (self.img_original.shape[1], self.img_original.shape[0]))
        heatmap_resize = np.uint8(255 * heatmap_resize)
        self.heatmapResizeImg1ch = heatmap_resize

        # applico una colormap per avere una heatmap simile a una immagine a colori
        colormap = cv2.COLORMAP_JET
        heatmap_colormap = cv2.applyColorMap(heatmap_resize, colormap)
        self.heatmapResizeImg = heatmap_colormap
        print_likearray_info(heatmap_colormap, 'heatmap_colormap')
        return heatmap_colormap

    def overlay_heatmap(self, alpha=0.5):
        # sovrappongo la heatmap all'immagine originale
        output = cv2.addWeighted(self.img_original, alpha, self.heatmapResizeImg, 1 - alpha, 0)

        # salvo " a portata di mano " la heatmap, l'immagine originale e quella sovrapposta
        print('salvo \" a portata di mano \" la heatmap, l\'immagine originale e quella sovrapposta')
        cv2.imwrite('./Notebook/3_CAMs/IMG/heatmap.jpg', self.heatmapResizeImg)
        cv2.imwrite('./Notebook/3_CAMs/IMG/imgOriginal.jpg', self.img_original)
        cv2.imwrite('./Notebook/3_CAMs/IMG/output.jpg', output)

        # restituisco una tupla con la heatmap e l'immagine overlaid
        return output

    def set_testBboxTxt(self, output, path_file_txt='./Notebook/3_CAMs/Bbox_txt/testBbox.txt'):
        try:
            os.remove(path_file_txt)
        except IOError:
            print("File dataVOC.csv non cancellato: non esiste")

        # reference : https://docs.opencv.org/master/d7/d1b/group__imgproc__misc.html#ggaa9e58d2860d4afa658ef70a9b1115576a95251923e8e22f368ffa86ba8bce87ff
        # per applicare cv.threshold devo avere una grayscale image : immagine ad 1 canale -> uso heatmapResizeImg1ch

        thresh = cv2.threshold(self.heatmapResizeImg1ch, 170, 255, cv2.THRESH_BINARY)[1]

        # Find contours
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            print(x, y, w, h)
            cv2.rectangle(thresh, (x, y), (x + w, y + h), (255, 255, 0), 3)
            cv2.rectangle(output, (x, y), (x + w, y + h), (255, 255, 255), 3)

            with open(path_file_txt, 'a') as a:
                a.write('{}, {}, {}, {}'.format(x, y, x + w, y + h))
                a.write('\n')

        # restituisco "tresh" e output con Bbox per stampa di debug
        return thresh, output

    def set_gtBboxTxt(self, output, anno_path, path_file_txt='./Notebook/3_CAMs/Bbox_txt/gtBbox.txt'):
        _, file_name = os.path.split(os.path.splitext(self.img_path)[0])
        anno_file = os.path.join(anno_path, file_name + '.xml')

        tree = ET.parse(anno_file)
        root = tree.getroot()

        countBbox = []

        try:
            os.remove(path_file_txt)
        except IOError:
            print("File dataVOC.csv non cancellato: non esiste")

        for obj in root.iter('object'):
            for bndbox in obj.iter('bndbox'):
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)
                countBbox.append(list((xmin, ymin, xmax, ymax)))
                cv2.rectangle(output, (xmin, ymin), (xmax, ymax), (200, 200, 0), 4)

                with open(path_file_txt, 'a') as a:
                    a.write('{}, {}, {}, {} '.format(xmin, ymin, xmax, ymax))
                    a.write('\n')
        print(countBbox)

        # restituisco output per stampa di debug
        return output

    if __name__ == "__main__":
        main()
