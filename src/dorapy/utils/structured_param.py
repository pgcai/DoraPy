'''
author:pgcai
date:20211009 22:44
'''
import copy
import numpy as np

class StructuredParam:
    '''
    A helper class represents network parameters or gradients
    helper类表示网络参数或梯度
    '''
    def __init__(self, param_list, nt_param_list=None):
        self.param_list = param_list
        self.nt_param_list = nt_param_list

    '''
    property是python的一种装饰器，是用来修饰方法的
    创建只读属性，@property装饰器会将方法转换为相同名称的只读属性
    可以与所定义的属性配合使用，这样可以防止属性被修改。
    '''
    @property
    def values(self):
        '''
        xxxx
        '''
        return np.array([v for p in self.param_list for v in p.values()], dtype=object)

    @values.setter
    def values(self, values):
        """
        xxx
        """
        i = 0
        for param in self.param_list:
            for name in param.keys():
                param[name] = values[i]
                i += 1
    
    @property
    def nt_values(self):
        """
        xxx
        """
        return np.array([v for p in self.nt_param_list for v in p.values()])

    @nt_values.setter
    def nt_values(self, values):
        """
        xxx
        """
        i = 0
        for param in self.nt_param_list:
            for name in param.keys():
                param[name] = values[i]
                i += 1

    @property
    def shape(self):
        '''
        xxx
        '''
        shape = list()
        for param in self.param_list:
            l_shape = dict()
            for key, val in param.items():
                l_shape[key] = val.shape
            shape.append(l_shape)
        shape = tuple(shape)    # 元组类型
        return shape
    
    @staticmethod       #python staticmethod 返回函数的静态方法。
    def _ensure_values(obj):
        '''
        函数功能未知
        '''
        if isinstance(obj, StructuredParam):    # isinstance() 函数来判断一个对象是否是一个已知的类型，类似 type()。
            obj = obj.values
        return obj

    def clip(self, min_=None, max_=None):
        obj = copy.deepcopy(self)   # 深复制
        obj.values = [v.clip(min_, max_) for v in self.values]
        return obj

    '''
    +
    这连着的三个add到底是在搞什么
    '''

    def __add__(self, other):
        obj = copy.deepcopy(self)
        obj.values = self.values + self._ensure_values(other)
        return obj

    def __radd__(self, other):
        obj = copy.deepcopy(self)
        obj.values = self._ensure_values(other) + self.values

    def __iadd__(self, other):
        self.values += self._ensure_values(other)
        return self

    '''
    -
    '''
    def __sub__(self, other):
        obj = copy.deepcopy(self)
        obj.values = self._ensure_values(other) - self.values
        return obj

    def __isub__(self, other):
        other = self._ensure_values(other)
        self.values -= self._ensure_values(other)
        return self

    def __mul__(self, other):
        obj = copy.deepcopy(self)
        obj.values = self.values * self._ensure_values(other)
        return obj
    
    def __rmul__(self, other):
        obj = copy.deepcopy(self)
        obj.values = self._ensure_values(other) * self.values
        return obj

    def __imul__(self, other):
        self.values *= self._ensure_values(other)
        return self

    def __truediv__(self, other):
        obj = copy.deepcopy(self)
        obj.values = self.values / self._ensure_values(other)
        return obj

    def __rtruediv__(self, other):
        obj = copy.deepcopy(self)
        obj.values = self._ensure_values(other) / self.values
        return obj

    def __itruediv__(self, other):
        self.values /= self._ensure_values(other)
        return self
    def __pow__(self, other):
        obj = copy.deepcopy(self)
        obj.values = self.values ** self._ensure_values(other)
        return obj

    def __ipow__(self, other):
        self.values **= self._ensure_values(other)
        return self

    def __neg__(self):
        obj = copy.deepcopy(self)
        obj.values = -self.values
        return obj

    def __len__(self):
        return len(self.values)

    def __lt__(self, other):
        obj = copy.deepcopy(self)
        other = self._ensure_values(other)

        if isinstance(other, (float, int)):
            obj.values = [v < other for v in self.values]
        else:
            obj.values = [v < other[i] for i, v in enumerate(self.values)]
        return obj

    def __gt__(self, other):
        obj = copy.deepcopy(self)
        other = self._ensure_values(other)

        if isinstance(other, (float, int)):
            obj.values = [v > other for v in self.values]
        else:
            obj.values = [v > other[i] for i, v in enumerate(self.values)]
        return obj

    def __le__(self, other):
        obj = copy.deepcopy(self)
        other = self._ensure_values(other)

        if isinstance(other, (float, int)):
            obj.values = [v <= other for v in self.values]
        else:
            obj.values = [v <= other[i] for i, v in enumerate(self.values)]
        return obj

    def __ge__(self, other):
        obj = copy.deepcopy(self)
        other = self._ensure_values(other)

        if isinstance(other, (float, int)):
            obj.values = [v >= other for v in self.values]
        else:
            obj.values = [v >= other[i] for i, v in enumerate(self.values)]
        return obj

    def __and__(self, other):
        obj = copy.deepcopy(self)
        obj.values = self._ensure_values(other) & self.values
        return obj

    def __or__(self, other):
        obj = copy.deepcopy(self)
        obj.values = self._ensure_values(other) | self.values
        return obj

    





















