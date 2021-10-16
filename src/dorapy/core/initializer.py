"""
Various of network parameter initializers
各种网络参数初始化器
"""

import numpy as np

'''
about class XavierNormal and class HeUniform
'''
def get_funs(shape):
    fan_in = shape[0] if len(shape) == 2 else np.prod(shape[1:])
    fan_out = shape[1] if len(shape) == 2 else shape[0]
    return fan_in, fan_out

class Initializer:


    def __call__(self, shape):
        return self.init(shape).astype(np.float32)

    def init(self, shape):
        raise NotImplementedError

"""
正态分布
"""
class Normal(Initializer):

    def __init__(self, mean=0.0, std=1.0):
        self._mean = mean
        self._std = std

    def init(self, shape):
        return np.random.normal(loc=self._mean, scale=self._std, size=shape)

'''
Truncated normal
截尾正态分布
'''
class TruncatedNormal(Initializer):

    def __init__(self, low, high, mean=0.0, std = 1.0):
        self._mean , self._std = mean, std
        self._low, self._high = low, high

    def init(self, shape):
        data = np.random.normal(loc=self._mean, scale=self._std, size=shape)
        while True:
            mask = (data > self._low) & (data < self._high)
            if mask.all():
                break
            data[~mask] = np.random.normal(loc=self._mean, scale=self._std, size=(~mask).sum)  # 不太理解
        return data

"""
随机生成[a,b]区间中的实数
"""
class Uniform(Initializer):

    def __init__(self, a=0.0, b=0.0):
        self._a = a
        self._b = b

    def init(self, shape):
        return np.random.uniform(low=self._a, high=self._b, size=shape)

"""
shape形状的值全为val
"""
class Constant(Initializer):

    def __init__(self, val):
        self._val = val

    def init(self, shape):
        return np.full(shape=shape, fill_value=self._val)

"""
值全为0
"""
class Zeros(Constant):

    def __init__(self):
        super(Zeros, self).__init__(0.0)

"""
值全为1
"""
class Ones(Constant):

    def __init__(self):
        super(Ones, self).__init__(1.0)


'''
Implement the Xavier method described in
"Understanding the difficulty of training deep feedforward neural networks"
Glorot, X. & Bengio, Y. (2010)

Weights will have values sampled from uniform distribution N(0, std) where
std = gain * sqrt(1.0 / (num_in + num_out))
'''
class XavierUniform(Initializer):
    '''
    xavier初始化方法
    pytorch的默认初始化方法
    '''
    def __init__(self, gain=1.0):
        self._gain = gain

    def init(self, shape):
        fan_in, fan_out = get_funs(shape)
        std = self._gain * np.sqrt(2.0 / (fan_in + fan_out))
        return np.random.normal(loc=0.0, scale=std, size=shape)

class HeUniform(Initializer):
    """
    Implement the He initialization method described in
    "Delving deep into rectifiers: Surpassing human-level performance
    on ImageNet classification" He, K. et al. (2015)

    Weights will have values sampled from uniform distribution U(-a, a) where
    a = sqrt(6.0 / num_in)
    """

    def __init__(self, gain=1.0):
        self._gain = gain
    
    def init(self, shape):
        fan_in, _ = get_funs(shape)
        a = self._gain * np.sqrt(6.0 * fan_in)
        return np.random.uniform(low=-a, high=a, size=shape)

class HeNormal(Initializer):
    """
    Implement the He initialization method described in
    "Delving deep into rectifiers: Surpassing human-level performance
    on ImageNet classification" He, K. et al. (2015)

    Weights will have values sampled from normal distribution N(0, std) where
    std = sqrt(2.0 / num_in)
    """
    def __init__(self, gain=1.0):
        self._gain = gain

    def init(self, shape):
        fan_in, _ = get_funs(shape)
        std = self._gain * np.sqrt(2.0 / fan_in)
        return np.random.normal(loc=0.0, scale=std, size=shape)










