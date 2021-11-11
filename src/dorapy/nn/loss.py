# 20210924
import numpy as np
import numpy as np
from dorapy.utils.math import log_softmax
from dorapy.utils.math import sigmoid
from dorapy.utils.math import softmax

class Loss():

    def loss(self, *args, **kwargs):
        raise NotImplementedError

    def grad(self, *args, **kwargs):
        raise NotImplementedError

class MSE(Loss):
    '''
    Mean squared error
    均方误差
    '''
    def loss(self, predictions, targets):
        # targets.shape[0] 就是 n
        return 0.5 * np.sum((predictions - targets) ** 2) / targets.shape[0]

    def grad(self, predictions, targets):
        # 梯度 
        return (predictions - targets) / targets.shape[0]

class MAE(Loss):
    '''
    平均绝对误差（Mean Absolute Error）
    '''

    def loss(self, predictions, targets):
        return np.sum(np.abs(predictions - targets)) / targets.shape[0]

    def grad(self, predictions, targets):
        return np.sign(predictions - targets) / targets.shape[0]

class Huber(Loss):
    '''
    Huber损失函数，平滑平均绝对误差
    相比平方误差损失，Huber损失对于数据中异常值的敏感性要差一些。
    在值为0时，它也是可微分的。它基本上是绝对值，在误差很小时会变为平方值。
    误差使其平方值的大小如何取决于一个超参数δ，该参数可以调整。
    当δ~ 0时，Huber损失会趋向于MSE；
    当δ~ ∞（很大的数字），Huber损失会趋向于MAE。
    '''

    def __init__(self, delta=1.0):
        self._delta = delta

    def loss(self, predictions, targets):
        l1_dist = np.abs(predictions - targets)
        mse_mask = l1_dist < self._delta    # MSE part
        mae_mask = ~mse_mask # MAE part
        mse = 0.5 * (predictions - targets) ** 2
        mae = self._delta * l1_dist - 0.5 * self._delta **2
        return np.sum(mse * mse_mask + mae * mae_mask) / targets.shape[0]

    def grad(self, predictions, targets):
        err = predictions - targets
        mse_mask = np.abs(err) < self._delta 
        mae_mask = ~mse_mask # MAE part
        mse_grad = err
        mae_grad = np.sign(err) * self._delta
        return (mae_grad * mae_mask + mse_grad * mse_mask) /targets.shape[0]

class SoftmaxCrossEntropy(Loss):
    '''
    在二分类或者类别相互排斥多分类问题，
    计算 logits 和 labels 之间的 softmax 交叉熵。
    '''
    
    def __init__(self, T=1.0, weights=None):
        self._weights = np.asarray(weights) if weights is not None else weights
        self._T = T

    def loss(self, logits, labels):
        nll = -(log_softmax(logits, t=self._T, axis=1) * labels).sum(axis=1)
        if self._weights is not None:
            nll *= self._weights[np.argmax(labels, axis=1)]
        return np.sum(nll) / labels.shape[0]

    def grad(self, logits, labels):
        grads = softmax(logits, t=self._T) - labels
        if self._weights is not None:
            grads *= self._weights
        return grads / labels.shape[0]

class SigmoidCrossEntropy(Loss):
    '''
    sigmoid_cross_entropy_with_logits函数，
    测量每个类别独立且不相互排斥的离散分类任务中的概率。
    '''
    def __init__(self, weights=None):
        weights = np.ones(2, dtypr=np.float32) if weights is None else weights
        self._weights = np.asarray(weights)

    def loss(self, logits, labels):
        neg_weight, pos_weight = self._weights
        cost = neg_weight * logits * (1 - labels) - \
        (pos_weight * labels - neg_weight * (labels - 1)) * \
            np.log(sigmoid(logits))
        return np.sum(cost) / labels.shape[0]
























