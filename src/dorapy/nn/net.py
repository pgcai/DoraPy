from dorapy.nn import layer
import copy
import numpy as np
from dorapy.utils.structured_param import StructuredParam

class Net(object):

    def __init__(self, layers):
        self.layers = layers
        self._is_training = True

    def __repr__(self):
        '''
        打印网络
        '''
        return '\n'.join([str(layer) for layer in self.layers])


    def forward(self, inputs):
        for layer in self.layers:
            inputs = layer.forward(inputs)
        return inputs

    def backward(self, grad):
        '''
        反向传播
        '''
        layer_grads = []
        for layer in reversed(self.layers):
            grad = layer.backward(grad)
            layer_grads.append(copy.copy(layer.grads))
        
        # return structured gradients
        struct_grad = StructuredParam(layer_grads[::-1])
        struct_grad.wrt_input = grad
        return struct_grad

    @property
    def params(self):
        trainable = [layer.params for layer in self.layers]
        non_trainable = [layer.nt_params for layer in self.layers]
        return StructuredParam(trainable, non_trainable)

    @params.setter
    def params(self, params):
        self.params.values = params.values
        self.params.nt_values = params.nt_values

    @property
    def is_training(self):
        return self._is_training

    @is_training.setter
    def is_training(self, is_training):
        for layer in self.layers:
            layer.is_training = is_training
        self._is_training = is_training

    def init_params(self, input_shape):
        # 手动初始化参数，让数据通过网络转发
        self.forward(np.ones((1, *input_shape)))




