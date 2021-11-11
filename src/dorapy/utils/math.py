'''
Useful math utilities.
数学公式库
'''
import numpy as np

def softmax(x, t=1.0, axis=-1):
    '''
    softmax函数
    '''
    x_ = x/t
    x_max = np.max(x_, axis=axis, keepdims=True)
    exps = np.exp(x_ - x_max)
    return exps / np.sum(exps, axis=axis, keepdims=True)

def log_softmax(x, t=1.0, axis=-1):
    '''
    log_softmax能够解决函数overflow和underflow
    加快运算速度，提高数据稳定性。
    '''
    x_ = x / t
    x_max = np.max(x_, axis=axis, keepdims=True)
    exps = np.exp(x_ - x_max)
    exp_sum = np.sum(exps, axis=axis, keepdims=True)
    return x_ - x_max - np.log(exp_sum)

def sigmoid(x):
    '''
    sigmoid函数
    '''
    x = np.asarray(x)
    ret = np.zeros_like(x, dtype=float)
    ret[x > 0] = 1.0 / (1.0 + np.exp(-x[x > 0]))
    a = np.exp(x[x <= 0])
    ret[x <= 0] = a/(1.0 + a)
    return ret















