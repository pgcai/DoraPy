#-coding: utf-8 -*-
'''
拟合曲线
author:pgcai
date:20211220
'''

'''
回归问题示例
曲线拟合示例
20211220
'''
import numpy as np
import matplotlib.pyplot as plt
import cv2 
import dorapy as nn
from dorapy.utils.mathTool import mae, rmse

np.random.seed(7)       # 随机种子设置为7时效果最好

def date():
    x = np.random.uniform(-np.pi, np.pi, 1000)    # x 坐标输入，50表示在0-2pi之间显示50个点
    a, b, c, d = 1, 2, 3, 4
    y = np.sin(x)    # 计算对应x的正弦值
    y = a*np.cos(b*x) + c*np.sin(d*x)
    
    plt.plot(x, y, 'b.')    #控制图形格式为蓝色带星虚线，显示正弦曲线，b表示蓝色，p表示型号，--表示虚线
    plt.show()    #显示图形

    train_x = x[:,np.newaxis]
    train_y = y[:,np.newaxis]

    x = np.random.uniform(-np.pi, np.pi, 100)
    y = a*np.cos(b*x) + c*np.sin(d*x)
    plt.plot(x, y, 'r.')    #控制图形格式为蓝色带星虚线，显示正弦曲线，b表示蓝色，p表示型号，--表示虚线
    plt.show()    #显示图形

    test_x = x[:,np.newaxis]
    test_y = y[:,np.newaxis]

    return train_x, train_y, test_x, test_y

def fc_model():
    net = nn.net.Net([
        nn.layer.Dense(1),
        nn.layer.Sigmoid(),
        nn.layer.Dense(16),
        nn.layer.Sigmoid(),
        nn.layer.Dense(32),
        nn.layer.Sigmoid(),
        nn.layer.Dense(32),
        nn.layer.Sigmoid(),
        nn.layer.Dense(16),
        nn.layer.Sigmoid(),
        nn.layer.Dense(1)
    ])
    return net

def evaluate(model, test_x, test_y):
    model.is_training = False
    test_pred = model.forward(test_x)

    print("rmse = ", rmse(test_y, test_pred))
    print("rmse = ", mae(test_y, test_pred))
    plt.plot(test_x, test_y, 'g.')    #控制图形格式为蓝色带星虚线，显示正弦曲线，b表示蓝色，p表示型号，--表示虚线
    plt.plot(test_x, test_pred, 'b.')    #控制图形格式为蓝色带星虚线，显示正弦曲线，b表示蓝色，p表示型号，--表示虚线
    plt.show()    #显示图形
    model.is_training = True

def main():
    train_x, train_y, test_x, test_y = date()
    print(train_x.shape)
    print(train_y.shape)

    lr = 1e-3
    batch_size = 32 
    batch = int(train_x.shape[0]/batch_size)
    print(batch)
    epoch = 9000

    net = fc_model()
    loss = nn.loss.MSE()
    optimizer = nn.optimizer.Adam(lr=lr)
    model = nn.model.Model(net=net, loss=loss, optimizer=optimizer)

    iterator = nn.data_iterator.BatchIterator(batch_size=batch_size)
    loss_list = list()

    plt.ion()  #interactive mode on

    for epoch in range(epoch):
        print("\r epoch = " + str(epoch), end='')
        for batch in iterator(train_x, train_y):
            pred = model.forward(batch.inputs)
            loss, grads = model.backward(pred, batch.targets)
            # print(loss)
            model.apply_grads(grads)
            loss_list.append(loss)
        
        if epoch % 50 == 0:
            plt.clf()
            model.is_training = False
            test_pred = model.forward(test_x)

            print("\nrmse = ", rmse(test_y, test_pred))
            print("mae = ", mae(test_y, test_pred))
            plt.plot(test_x, test_y, 'g.')    #控制图形格式为蓝色带星虚线，显示正弦曲线，b表示蓝色，p表示型号，--表示虚线
            plt.plot(test_x, test_pred, 'b.')    #控制图形格式为蓝色带星虚线，显示正弦曲线，b表示蓝色，p表示型号，--表示虚线
            # plt.show()    #显示图形
            plt.draw()
            plt.pause(0.01)
            model.is_training = True

    # evaluate
    print(net)
    evaluate(model, test_x, test_y)


if __name__ == '__main__':
    main()