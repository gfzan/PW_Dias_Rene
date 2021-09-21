from src.heatmap.image import Image
import numpy as np
import cv2


class IoU:
    # ATTRIBUTI:
    iou = []
    intersections = []

    def __init__(self, gtBboxPath, testBboxPath, img_path):
        self.gtBboxList = self.list_bbox(gtBboxPath)
        self.testBboxList = self.list_bbox(testBboxPath)
        self.__image = Image(img_path).get_image_copy()

    @staticmethod
    def list_bbox(path_bbox):
        with open(path_bbox, "r") as f:
            arr_bbox = [line.split(",") for line in f.read().splitlines()]
        arr_bbox = np.array([[int(j) for j in i] for i in arr_bbox])
        return arr_bbox

    @staticmethod
    def computeIoU(boxA, boxB):
        # punti delle intersezioni (rettangoli)
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])

        # calcolo area dele intersezioni
        interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

        # somma delle aree dei boundig box gt+test
        boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
        boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

        # calcolo IoU
        iou = interArea / float(boxAArea + boxBArea - interArea)

        # restituisco IoU e rettangoli di intersezione
        if interArea > 0:
            intersection = [xA, yA, xB, yB]
        else:
            intersection = 0

        return iou, intersection

    def set_listIoU(self):
        for i in self.testBboxList:
            for j in self.gtBboxList:
                self.iou.append(self.computeIoU(i, j)[0])
                if isinstance(self.computeIoU(i, j)[1], list):
                    self.intersections.append(self.computeIoU(i, j)[1])

    def plotBbox(self):
        image_bbox = self.__image.copy()

        for i in self.testBboxList:
            for j in self.gtBboxList:
                cv2.rectangle(image_bbox, (i[0], i[1]), (i[2], i[3]), (0, 255, 0), 2)
                cv2.rectangle(image_bbox, (j[0], j[1]), (j[2], j[3]), (0, 0, 255), 2)

        cv2.putText(image_bbox, "IoU: {:.4f}".format(np.max(self.iou)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (0, 255, 0), 2)
        print(f' IoU immagine selezionata : {np.max(self.iou) :.4f}')

        image_area = self.__image.copy()
        for w in self.intersections:
            cv2.rectangle(image_area, (w[0], w[1]), (w[2], w[3]), (0, 255, 0), -2)

        horizontal_concat_image = np.concatenate((image_bbox, image_area), axis=1)

        # stampo le immagini (image_bbox, image_area)
        cv2.imshow('Horizontal Concat', horizontal_concat_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
