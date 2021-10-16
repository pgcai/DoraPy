# model.py
# 20210924
# 加油
"""
Model class manage 
the network, 
loss function 
and optimizer.
"""

import pickle

class Model(object):
    def __init__(self, net, loss, optimizer):
        '''
        model初始化
        '''
        self.net = net
        self.loss = loss
        self.optimizer = optimizer

    def forward(self, inputs):
        '''
        前向传播
        '''
        return self.net.forward(inputs)
        

    def backward(self, predictions, targets):
        '''
        反向传播
        计算损失、梯度
        '''
        loss = self.loss.loss(predictions, targets)
        grad_from_loss = self.loss.grad(predictions, targets)
        struct_grad = self.net.backward(grad_from_loss)
        return loss, struct_grad

    def apply_grads(self, grads):
        '''
        利用求出的梯度更新网络
        '''
        params = self.net.params
        self.optimizer.step(grads, params)

    def save(self, path):
        '''
        保存网络
        '''
        with open(path, "wb") as f:
            pickle.dump(self.net.params, f)
    
    def load(self, path):
        '''
        加载模型
        '''
        with open(path, 'rb') as f:
            params = pickle.load(f)
        
        self.net.params = params
        for layer in self.net.layers:
            layer.is_init = True

    @property
    def is_training(self):
        return self.net.is_training
    
    @is_training.setter
    def is_training(self, is_training):
        self.net.is_training = is_training
    
    