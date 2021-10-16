'''
Common datasets
常见的数据集
'''

import gzip
import os
import pickle
import struct
import tarfile

import numpy as np
from numpy.core.numeric import ones

from dorapy.utils.downloader import download_url

class Dataset:

    def __init__(self, data_dir, **kwargs):
        self._train_set = None      # 训练集
        self._valid_set = None      # 验证集
        self._test_set = None       # 测试集

        self._save_paths = [os.path.join(data_dir,
        url.split('/')[-1]) for url in self._urls]
        self._download()
        self._parse(**kwargs)

    def _download(self):
        for url, checksum, save_path in zip(self._urls, self._checksums, self._save_paths):
            download_url(url ,save_path, checksum)
    
    def _parse(self, **kwargs):
        raise NotImplementedError

    @property
    def train_set(self):
        '''
        返回训练集
        '''
        return self._train_set

    @property
    def valid_set(self):
        '''
        返回验证集
        '''
        return self._valid_set

    @property
    def test_set(self):
        '''
        返回测试集
        '''
        return self._test_set

    @staticmethod
    def get_one_hot(targets, n_classes):
        '''
        label2one-hot
        '''
        return np.eye(n_classes)[np.array(targets).reshape(-1)]


class MNIST(Dataset):

    def __init__(self, data_dir, one_hot=True):
        self._urls = ("https://raw.githubusercontent.com/mnielsen/neural-networks-and-deep-learning/master/data/mnist.pkl.gz",)
        self._checksums = ("98100ca27dc0e07ddd9f822cf9d244db",)
        self._n_classes = 10
        super().__init__(data_dir, one_hot=one_hot)

    def _parse(self, **kwargs):
        save_path = self._save_paths[0]
        with gzip.open(save_path, "rb") as f:
            train, valid, test = pickle.load(f, encoding="latin1")

        if kwargs["one_hot"]:
            train = (train[0], self.get_one_hot(train[1], self._n_classes))
            valid = (valid[0], self.get_one_hot(valid[1], self._n_classes))
            test = (test[0], self.get_one_hot(test[1], self._n_classes))

        self._train_set, self._valid_set, self._test_set = train, valid, test



class FashionMNIST(Dataset):
    pass

class Cifar(Dataset):
    pass

class Cifar10(Cifar):
    pass

class Cifar100(Cifar):
    pass











    