from tensorflow.keras.models import load_model


class ConvNet:
    # COSTANTI
    CLASS_IMAGE = ('bird', 'cat', 'dog', 'person')

    def __init__(self, path_model, classifier_layer_names, last_conv_layer_name):
        self.path_model = path_model
        self.classifier_layer_names = classifier_layer_names
        self.saved_model = self.__set_model(path_model)
        if last_conv_layer_name is None:
            self.last_conv_layer_name = self.__set_last_layername()
        else:
            self.last_conv_layer_name = last_conv_layer_name

    def __set_last_layername(self):
        saved_layer = None
        for layer in self.saved_model.layers:
            # seleziono ultimo strato conv, se c'è!
            try:
                if len(layer.output_shape) == 4 and 'conv' in layer.name:
                    saved_layer = layer.name
            except ValueError:
                print('NON SI TROVA layer conv non si può applicare HEATMAP')
        return saved_layer

    @staticmethod
    def __set_model(path):
        model = []
        try:
            model = load_model(path)
        except OSError:
            print("FILE errato o PERCORSO non esistente")
        return model
