# layer.py
# pgcai 20210921
import numpy as np
from dorapy.nn.initializer import Ones
from dorapy.nn.initializer import XavierUniform
from dorapy.nn.initializer import Zeros
from dorapy.utils.math import sigmoid


class Layer():
    '''
    Base class for layers.
    神经网络层的基类
    '''
    def __init__(self):
        self.params = {p: None for p in self.param_names}
        self.nt_params = {p: None for p in self.nt_param_names}
        self.initializers = None

        self.grads = {}
        self.shapes = {}

        self._is_training = True    # used in BatchNorm/Dropout layers
        self._is_init = False

    def forward(self, inputs):
        raise NotImplementedError

    def backward(self, grad):
        raise NotImplementedError

    
    @property
    def is_init(self):
        return self._is_init

    @is_init.setter
    def is_init(self, is_init):
        self._is_init = is_init
        for name in self.param_names:
            self.shapes[name] = self.params[name].shape
    
    @property
    def is_training(self):
        return self._is_training

    @is_training.setter
    def is_training(self, is_train):
        self._is_training = is_train

    @property
    def name(self):
        return self.__class__.__name__

    def __repr__(self):
        '''
        显示属性
        '''
        shape = None if not self.shapes else self.shapes
        return f'layer: {self.name}\tshape:{shape}'

    @property
    def param_names(self):
        return ()

    @property
    def nt_param_names(self):
        return ()

    def _init_params(self):
        for name in self.param_names:
            self.params[name] = self.initializers[name](self.shapes[name])
        self.is_init = True
    



class Dense(Layer):
    '''
    全连接层。
    Fully connected layer.
    '''
    def __init__(
        self,
        num_out,
        w_init=XavierUniform(),     # XavierUniform初始化
        b_init=Zeros()):
        super().__init__()
        
        self.initializers = {'w': w_init, 'b': b_init}
        self.shapes = {'w': [None, num_out], 'b': [num_out]}

        self.ctx = None


    def forward(self, inputs):
        if not self.is_init:
            self.shapes["w"][0] = inputs.shape[1]
            self._init_params()
        self.ctx = {"inputs":inputs}
        return inputs @ self.params["w"] + self.params["b"]    # @ 矩阵-向量乘法

    def backward(self, grad):
        self.grads["w"] = self.ctx["inputs"].T @ grad
        self.grads['b'] = np.sum(grad, axis=0)
        return grad @ self.params["w"].T

    @property
    def param_names(self):
        return "w", "b"
    

class Conv2D(Layer):

    def __init__(
        self,
        kernel,
        stride=(1, 1),
        padding="SAME",
        w_init=XavierUniform(),
        b_init=Zeros()):
        super().__init__()

        self.kernel_shape = kernel
        self.stride = stride
        self.initializers = {"w": w_init, "b": b_init}
        self.shapes = {"w": self.kernel_shape, "b": self.kernel_shape[-1]}

        self.padding_mode = padding
        self.padding = None

        self.ctx = None

    def forward(self, inputs):

        if not self.is_init:
            self._init_params()

        k_h, k_w, _, out_c = self.kernel_shape
        s_h, s_w = self.stride
        X = self._inputs_preprocess(inputs)

        # padded inputs to column matrix
        # 填充输入到列矩阵
        col = im2col(X, k_h, k_w, s_h, s_w)
        # perform convolution by matrix product.
        # 通过矩阵乘积进行卷积。
        W = self.params["w"].reshape(-1, out_c)
        Z = col @ W
        # reshape output
        batch_sz, in_h, in_w, _ = X.shape
        # separate the batch size and feature map dimmensions
        # 分离batch size和feature map尺寸
        Z = Z.reshape(batch_sz, Z.shape[0] // batch_sz, out_c)
        # further divide the feature map in to (h, w) dimension
        # 进一步将特征图划分为(h, w)维度
        out_h = (in_h - k_h) // s_h + 1
        out_w = (in_w - k_w) // s_w + 1
        Z = Z.reshape(batch_sz, out_h, out_w, out_c)

        # plus the bias for every filter
        Z += self.params["b"]
        # save results for backward function
        self.ctx = {"X_shape": X.shape, "col": col, "W": W}
        return Z
    
    def backward(self, grad):
        """Compute gradients w.r.t layer parameters and backward gradients.
        :param grad: gradients from previous layer
            with shape (batch_sz, out_h, out_w, out_c)
        :return d_in: gradients to next layers
            with shape (batch_sz, in_h, in_w, in_c)
        """
        # read size parameters
        k_h, k_w, in_c, out_c = self.kernel_shape
        s_h, s_w = self.stride
        batch_sz, in_h, in_w, in_c = self.ctx["X_shape"]
        pad_h, pad_w = self.padding[1:3]

        # grads w.r.t parameters
        flat_grad = grad.reshape((-1, out_c))
        d_W = self.ctx["col"].T @ flat_grad
        self.grads["w"] = d_W.reshape(self.kernel_shape)
        self.grads["b"] = np.sum(flat_grad, axis=0)

        # grads w.r.t inputs
        d_X = grad @ self.ctx["W"].T
        # cast gradients back to original shape as d_in
        d_in = np.zeros(shape=self.ctx["X_shape"])
        for i, r in enumerate(range(0, in_h - k_h + 1, s_h)):
            for j, c in enumerate(range(0, in_w - k_w + 1, s_w)):
                patch = d_X[:, i, j, :]
                patch = patch.reshape((batch_sz, k_h, k_w, in_c))
                d_in[:, r:r+k_h, c:c+k_w, :] += patch

        # cut off gradients of padding
        d_in = d_in[:, pad_h[0]:in_h-pad_h[1], pad_w[0]:in_w-pad_w[1], :]
        return self._grads_postprocess(d_in)

    def _inputs_preprocess(self, inputs):
        _, in_h, in_w, _ = inputs.shape
        k_h, k_w, _, _ = self.kernel_shape
        # padding calculation
        if self.padding is None:
            self.padding = get_padding_2d(
                (in_h, in_w), (k_h, k_w), self.padding_mode)
        return np.pad(inputs, pad_width=self.padding, mode="constant")

    def _grads_postprocess(self, grads):
        return grads

    @property
    def param_names(self):
        return "w", "b"



class ConvTranspose2D(Conv2D):
    '''
    逆卷积
    '''
    pass

class MaxPool2D(Layer):
    def __init__(self,
                 pool_size=(2, 2),
                 stride=None,
                 padding="VALID"):
        """Implement 2D max-pooling layer
        :param pool_size: A list/tuple of 2 integers (pool_height, pool_width)
        :param stride: A list/tuple of 2 integers (stride_height, stride_width)
        :param padding: A string ("SAME", "VALID")
        """
        super().__init__()
        self.kernel_shape = pool_size
        self.stride = stride if stride is not None else pool_size

        self.padding_mode = padding
        self.padding = None

        self.ctx = None

    def forward(self, inputs):
        s_h, s_w = self.stride
        k_h, k_w = self.kernel_shape
        batch_sz, in_h, in_w, in_c = inputs.shape

        # zero-padding
        if self.padding is None:
            self.padding = get_padding_2d(
                (in_h, in_w), (k_h, k_w), self.padding_mode)
        X = np.pad(inputs, pad_width=self.padding, mode="constant")
        padded_h, padded_w = X.shape[1:3]

        out_h = (padded_h - k_h) // s_h + 1
        out_w = (padded_w - k_w) // s_w + 1

        # construct output matrix and argmax matrix
        max_pool = np.empty(shape=(batch_sz, out_h, out_w, in_c))
        argmax = np.empty(shape=(batch_sz, out_h, out_w, in_c), dtype=int)
        for r in range(out_h):
            r_start = r * s_h
            for c in range(out_w):
                c_start = c * s_w
                pool = X[:, r_start: r_start+k_h, c_start: c_start+k_w, :]
                pool = pool.reshape((batch_sz, -1, in_c))

                _argmax = np.argmax(pool, axis=1)[:, np.newaxis, :]
                argmax[:, r, c, :] = _argmax.squeeze()

                # get max elements
                _max_pool = np.take_along_axis(pool, _argmax, axis=1).squeeze()
                max_pool[:, r, c, :] = _max_pool

        self.ctx = {"X_shape": X.shape, "out_shape": (out_h, out_w),
                    "argmax": argmax}
        return max_pool

    def backward(self, grad):
        batch_sz, in_h, in_w, in_c = self.ctx["X_shape"]
        out_h, out_w = self.ctx["out_shape"]
        s_h, s_w = self.stride
        k_h, k_w = self.kernel_shape
        k_sz = k_h * k_w
        pad_h, pad_w = self.padding[1:3]

        d_in = np.zeros(shape=(batch_sz, in_h, in_w, in_c))
        for r in range(out_h):
            r_start = r * s_h
            for c in range(out_w):
                c_start = c * s_w
                _argmax = self.ctx["argmax"][:, r, c, :]
                mask = np.eye(k_sz)[_argmax].transpose((0, 2, 1))
                _grad = grad[:, r, c, :][:, np.newaxis, :]
                patch = np.repeat(_grad, k_sz, axis=1) * mask
                patch = patch.reshape((batch_sz, k_h, k_w, in_c))
                d_in[:, r_start:r_start+k_h, c_start:c_start+k_w, :] += patch

        # cut off gradients of padding
        return d_in[:, pad_h[0]:in_h-pad_h[1], pad_w[0]:in_w-pad_w[1], :]

class RNN(Layer):
    '''
    rnn(卷积神经网络)
    '''
    pass

class BatchNormalization(Layer):
    '''
    批量归一化
    '''
    pass

class Reshape(Layer):
    '''
    reshape
    '''
    def __init__(self, *output_shape):
        super().__init__()
        self.output_shape = output_shape
        self.input_shape = None

    def forward(self, inputs):
        self.input_shape = inputs.shape
        return inputs.reshape(inputs.shape[0], *self.output_shape)

    def backward(self, grad):
        return grad.reshape(self.input_shape)

class Flatten(Reshape):
    '''
    all_shape2a_line
    '''
    def __init__(self):
        super().__init__(-1)

class Dropout(Layer):
    '''
    dropout
    '''
    pass

class Activation(Layer):
    '''Base activation layer'''

    def __init__(self):
        super().__init__()
        self.inputs = None

    def forward(self, inputs):
        self.inputs = inputs
        return self.func(inputs)

    def backward(self, grad):
        return self.derivative_func(self.inputs)*grad

    def func(self, x):
        raise NotImplementedError

    def derivative(self, x):
        raise NotImplementedError

class Sigmoid(Activation):
    '''
    sigmoid激活函数
    '''
    pass

class Softplus(Activation):
    '''
    softplus激活函数
    '''
    pass


class Tanh(Activation):
    '''
    tanh激活函数
    '''
    pass


class ReLU(Activation):
    '''ReLU activation function'''

    def func(self, x):
        return np.maximum(x, 0.0)
    
    def derivative_func(self, x):
        return x > 0.0


class LeakyReLU(Activation):
    '''
    leakyrelu激活函数
    '''
    pass

class GELU(Activation):
    '''
    gelu激活函数
    '''
    pass

class ELU(Activation):
    '''
    elu激活函数
    '''
    pass

def im2col(img, k_h, k_w, s_h, s_w):
    """Transform padded image into column matrix.
    :param img: padded inputs of shape (B, in_h, in_w, in_c)
    :param k_h: kernel height
    :param k_w: kernel width
    :param s_h: stride height
    :param s_w: stride width
    :return col: column matrix of shape (B*out_h*out_w, k_h*k_h*inc)
    """
    batch_sz, h, w, in_c = img.shape
    # calculate result feature map size
    out_h = (h - k_h) // s_h + 1
    out_w = (w - k_w) // s_w + 1
    # allocate space for column matrix
    col = np.empty((batch_sz * out_h * out_w, k_h * k_w * in_c))
    # fill in the column matrix
    batch_span = out_w * out_h
    for r in range(out_h):
        r_start = r * s_h
        matrix_r = r * out_w
        for c in range(out_w):
            c_start = c * s_w
            patch = img[:, r_start: r_start+k_h, c_start: c_start+k_w, :]
            patch = patch.reshape(batch_sz, -1)
            col[matrix_r+c::batch_span, :] = patch
    return col

def get_padding_2d(in_shape, k_shape, mode):
    def get_padding_1d(w, k):
        if mode == "SAME":
            pads = (w - 1) + k - w
            half = pads // 2
            padding = (half, half) if pads % 2 == 0 else (half, half + 1)
        else:
            padding = (0, 0)
        return padding

    h_pad = get_padding_1d(in_shape[0], k_shape[0])
    w_pad = get_padding_1d(in_shape[1], k_shape[1])
    return (0, 0), h_pad, w_pad, (0, 0)













