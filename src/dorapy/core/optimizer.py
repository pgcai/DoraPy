# optimizer.py
# 20210924
# hhhhhhh💪
"""
Various optimization algorithms and learning rate schedulers.
各种优化算法和学习率调度器。
"""
import numpy as np


class Optimizer:

    def __init__(self, lr, weight_decay):
        self.lr = lr
        self.weight_decay = weight_decay

    def step(self, grads, params):
        '''
        计算梯度步长compute the gradient step

        '''
        grads = self.compute_step(grads)
        # 应用权重衰减
        if self.weight_decay:
            grads -= self.lr * self.weight_decay * params
        
        params += grads


    def compute_step(self, grads):
        grads.values = self._compute_step(grads.values)
        return grads

    def _compute_step(self, grad):
        raise NotImplementedError


class Adam(Optimizer):
    '''
    Adam优化算法
    '''
    def __init__(
        self,
        lr=1e-3,        # 学习率    
        beta1=0.9,      # 一阶矩估计的指数衰减率
        beta2=0.999,    # 二阶矩估计的指数衰减率    在超参数稀疏梯度中，应设置为接近1的数
        epsilon=1e-8,   # 设置一个非常小的数,其用于防止在实习那种除以零
        weight_decay=0.0):
        super().__init__(lr, weight_decay)
        self._b1, self._b2 = beta1, beta2
        self._epsilon = epsilon

        self._t, self._m, self._v = 0, 0, 0

    def _compute_step(self, grad):

        self._t += 1

        self._m = self._b1 * self._m + (1 - self._b1) * grad
        self._v = self._b2 * self._v + (1 - self._b2) * (grad ** 2)

        # bias correction
        _m = self._m / (1 - self._b1 ** self._t)
        _v = self._v / (1 - self._b2 ** self._t)

        return -self.lr * _m / (_v ** 0.5 + self._epsilon)


class RAdam(Optimizer):
    """
    修正Adam
    Rectified Adam. 
    Ref: https://arxiv.org/pdf/1908.03265v1.pdf """
    pass


class RMSProp(Optimizer):
    """
    均方根支柱优化器
    Root Mean Square Prop optimizer
    mean_square = decay * mean_square{t-1} + (1-decay) * grad_t**2
    mom = momentum * mom{t-1} + lr * grad_t / sqrt(mean_square + epsilon)
    """
    pass


class Momentum(Optimizer):
    """
    基于梯度的移动指数加权平均
    accumulation = momentum * accumulation + gradient
    variable -= learning_rate * accumulation
    """
    pass

class Adagrad(Optimizer):
    """
    自动变更学习速率
    AdaGrad optimizer
    accumulation = - (learning_rate / sqrt(G + epsilon)) * gradient
    where G is the element-wise sum of square gradient
    ref: http://www.jmlr.org/papers/volume12/duchi11a/duchi11a.pdf
    """
    pass

class Adadelta(Optimizer):
    """
    AdaDelta算法主要是为了解决AdaGrad算法中存在的缺陷
    Adadelta algorithm (https://arxiv.org/abs/1212.5701)
    """
    pass


class BaseScheduler:
    """BaseScheduler model receive a optimizer and Adjust the lr
    by calling step() method during training.
    基础调度器模型接收一个优化器并调整lr
    通过在训练期间调用step()方法。
    """
    pass

class StepLR(BaseScheduler):
    """
    LR在每一个“步长”时期都被伽马衰减
    LR decayed by gamma every "step_size" epochs.
    """
    pass

class MultiStepLR(BaseScheduler):
    """
    当#steps达到一个里程碑时，LR会以gamma衰减。
    里程碑必须单调递增。
    LR decayed by gamma when #steps reaches one of the milestones.
    Milestones must be monotonically increasing.
    """
    pass

class ExponentialLR(BaseScheduler):
    """
    指数lr
    ExponentialLR is computed by:
    lr_decayed = lr * decay_rate ^ (current_steps / decay_steps)
    """
    pass

class LinearLR(BaseScheduler):
    """Linear decay learning rate when the number of the epoch is in
    [start_step, start_step + decay_steps]

    当epoch在[start_step, start_step + decay_steps]之间时，学习率线性下降
    """
    pass


class CyclicalLR(BaseScheduler):
    '''
    Cyclical increase and decrease learning rate 
    within a reasonable range.
    Ref: https://arxiv.org/pdf/1506.01186.pdf
    在合理范围内周期性增减学习率。
    '''
    pass

