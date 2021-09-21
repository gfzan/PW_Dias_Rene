# from src.heatmap.conv_net import ConvNet
import numpy as np

list_classes = ('bird', 'cat', 'dog', 'person')


def print_likearray_info(obj, obj_name):
    print('****************************************************')
    print(' STAMPA \"debug\"')
    print(f' TIPO \033[1m {obj_name} \033[0m = {type(obj)} \n'
          f' SHAPE \033[1m {obj_name} \033[0m = {obj.shape}')
    print(f' MAX {obj_name} MAX = {np.max(obj)} \n MIN {obj_name} MIN = {np.min(obj)}')
    print('****************************************************')


def prediction(preds):
    # calcolo/predico la classe e la stampo
    print('\n****************************************************')
    print('Prediction : ')
    for i in range(len(preds[0])):
        print(f'{list_classes[i]} \t = {preds[0][i]:.3f}%')
    print('Prediction : {} \n preds shape = {}'.format(preds[0], preds.shape))
    print('****************************************************\n')
