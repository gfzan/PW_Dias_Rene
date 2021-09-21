from src.heatmap.heatmap import Heatmap
from src.utils import *
import tensorflow as tf

import numpy as np


class HeatmapGradCam(Heatmap):

    def main(self):
        pass

    # COSTRUTTORE
    def __init__(self, img_path, path_model, classifier_layer_names, last_conv_layer_name=None):
        super(HeatmapGradCam, self).__init__(img_path, path_model, classifier_layer_names, last_conv_layer_name)

    def gradcam_heatmap(self, img_array):
        # creo modello CNN che estrae l'attivazione dell'ultimo layer conv

        last_conv_layer = self.conv_model.saved_model.get_layer(self.conv_model.last_conv_layer_name)
        gradcam_model = tf.keras.Model(self.conv_model.saved_model.inputs, last_conv_layer.output)

        # creo restante parte del modello che classifica i dati
        classifier_input = tf.keras.Input(shape=last_conv_layer.output.shape[1:])
        x = classifier_input
        for layer_name in self.classifier_layer_names:
            x = self.conv_model.saved_model.get_layer(layer_name)(x)
        classifier_model = tf.keras.Model(classifier_input, x)

        # calcolo il gradiente rispetto alla classe predetta
        with tf.GradientTape() as tape:
            # valori di attivazione dell'ultimo layer conv
            last_conv_layer_output = gradcam_model(img_array)
            print_likearray_info(last_conv_layer_output, 'last_conv_layer_output')

            tape.watch(last_conv_layer_output)
            # predizione della classe
            preds = classifier_model(last_conv_layer_output)
            top_pred_index = tf.argmax(preds[0])

            prediction(preds)

            top_class_channel = preds[:, top_pred_index]

        # gradiente calcolato rispetto alla predizione e all'input
        grads = tape.gradient(top_class_channel, last_conv_layer_output)

        # media del prodotto dello specifico gradiente per il singolo canale dello strato conv
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

        # prodotto dello strato di attivazione rispetto alla classe predetta
        last_conv_layer_output = last_conv_layer_output.numpy()[0]
        pooled_grads = pooled_grads.numpy()
        for i in range(pooled_grads.shape[-1]):
            last_conv_layer_output[:, :, i] *= pooled_grads[i]

        # la media per riga dello strato con di attivazione costituisce la heatmap
        heatmap = np.mean(last_conv_layer_output, axis=-1)

        # heatmap normalizzata
        heatmap = np.maximum(heatmap, 0) / np.max(heatmap)
        self.heatmap = heatmap
        print_likearray_info(heatmap, 'heatmap')

        return heatmap

    if __name__ == "__main__":
        main()
