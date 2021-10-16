'''
Data Iterator class.
数据迭代器
'''

from collections import  namedtuple
# collections模块的namedtuple子类不仅可以使用item的index访问item，还可以通过item的name进行访问。可以将namedtuple理解为c中的struct结构
# 其首先将各个item命名，然后对每个item赋予数据。

import numpy as np

Batch = namedtuple("Batch", ['inputs', 'targets'])

class BaseIterator:

    def __call__(self, inputs, targets):
        raise NotImplementedError

class BatchIterator(BaseIterator):
    def __init__(self, batch_size=32, shuffle=True):
        # shuffle  打乱顺序
        self._batch_size = batch_size
        self._shuffle = shuffle

    def __call__(self, inputs, targets):
        indices = np.arange(len(inputs))
        # indices index的复数 这里指目录
        # 这一步indices 的输出为[0, 1, 2 ... len(inputs)]
        if self._shuffle:   # 如果shuffle==true
            np.random.shuffle(indices)      # 打乱顺序
        
        
        starts = np.arange(0, len(inputs), self._batch_size)
        # 这一步starts的输出为[0, _batch_size, _batch_size*2, ... len(inputs)]
        for start in starts:
            end = start + self._batch_size
            batch_inputs = inputs[indices[start: end]]
            batch_targets = targets[indices[start: end]]
            '''
            带yield的函数是一个生成器，而不是一个函数了，
            这个生成器有一个函数就是next函数，
            next就相当于“下一步”生成哪个数，
            这一次的next开始的地方是接着上一次的next停止的地方执行的
            '''
            yield Batch(inputs=batch_inputs, targets=batch_targets)




