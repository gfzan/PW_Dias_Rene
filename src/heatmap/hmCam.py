from src.heatmap.heatmap import Heatmap
from src.utils import *
import tensorflow as tf

import numpy as np


class HeatmapCam(Heatmap):

    def main(self):
        pass

    # COSTRUTTORE
    def __init__(self, img_path, path_model, classifier_layer_names, last_conv_layer_name=None):
        super(HeatmapCam, self).__init__(img_path, path_model, classifier_layer_names, last_conv_layer_name)

    def cam_heatmap(self, img_array):
        last_conv_layer = self.conv_model.saved_model.get_layer(self.conv_model.last_conv_layer_name)
        cam_model = tf.keras.Model(self.conv_model.saved_model.inputs,
                                   (last_conv_layer.output, self.conv_model.saved_model.output))

        # estraggo l'attivazione dell'ultimo layer conv e predizione
        (lastConv_outputs, preds) = cam_model.predict(img_array)
        top_pred_index = tf.argmax(preds[0])

        last_conv_output = lastConv_outputs[0, :, :, :]  # prendo l'unico valore (immagine) del batch
        print_likearray_info(lastConv_outputs, 'lastConv_outputs')

        prediction(preds)

        # Estraggo i pesi dell'ultimo layer
        class_weights = cam_model.layers[-1].get_weights()[0]
        # print('class_weights shape = ', class_weights.shape)    -> output =    class_weights shape =  (1024, 4)
        print_likearray_info(class_weights, 'class_weights')

        # Create the class activation map.
        cam = np.zeros(shape=last_conv_output.shape[0:2], dtype=np.float32)

        for i, w in enumerate(class_weights[:]):
            cam += w[top_pred_index] * last_conv_output[:, :, i]
        cam /= np.max(cam)
        print_likearray_info(cam, 'cam')

        self.heatmap = cam

        # trasformazione da inserire dopo getCamForImg(self)!
        cam[np.where(cam < 0.2)] = 0
        return cam

    if __name__ == "__main__":
        main()
