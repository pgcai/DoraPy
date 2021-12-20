# -*- coding:utf-8 -*-  
"""  
@author:pgcai
@file:svm.py  
@func:Use SVM to achieve missile hit classification  
@time:2021/12/02 10:55AM
"""  
import sys
sys.path.append(r'./')      # 为了能找到自写函数
from scipy.sparse import data
from sklearn import tree
import numpy as np  
import matplotlib.pyplot as plt  
import matplotlib  
import sklearn  
from sklearn.model_selection import train_test_split
from utils.getdata import getdata
  
# define converts(字典)  
def hit_label(s):  
    it={b'unhit':0, b'hit':1}  
    return it[s]
  

#1.读取数据集 划分数据与标签
file_path = "./data/jg.xlsx"
inputdim = [16, 17, 18, 19, 20, 21, 54, 55, 56, 57]
outputdim = [6]
x, y = getdata(file_path, inputdim, outputdim)
train_rate = 0.7
train_data, test_data, train_label, test_label =train_test_split(x, y, random_state=1, train_size=train_rate) # sklearn.model_selection.  
print('train_data.shape = ', train_data.shape)
print('test_data.shape = ', test_data.shape)
print('train_label.shape = ', train_label.shape)
print('test_label.shape = ', test_label.shape)
print("--------------------------------------")

#3.训练决策树分类器  
classifier=tree.DecisionTreeClassifier(criterion='entropy',splitter='random', max_depth=4)
classifier.fit(train_data, train_label.ravel()) #ravel函数在降维时默认是行序优先  
  
# #4.计算准确率  
# print("训练集：",classifier.score(train_data,train_label))  
# print("测试集：",classifier.score(test_data,test_label))  
  
#也可直接调用accuracy_score方法计算准确率  
from sklearn.metrics import accuracy_score  
tra_label=classifier.predict(train_data) #训练集的预测标签  
tes_label=classifier.predict(test_data) #测试集的预测标签  
print("训练集：", accuracy_score(train_label,tra_label) )  
print("测试集：", accuracy_score(test_label,tes_label) )  
  
#查看 
print('predict_result:\n',classifier.predict(train_data))  
  
# #5.绘制图形  
# #确定坐标轴范围  
# x1_min, x1_max=x[:,0].min(), x[:,0].max() #第0维特征的范围  
# x2_min, x2_max=x[:,1].min(), x[:,1].max() #第1维特征的范围  
# x1,x2=np.mgrid[x1_min:x1_max:200j, x2_min:x2_max:200j ] #生成网络采样点  
# grid_test=np.stack((x1.flat,x2.flat) ,axis=1) #测试点  
# #指定默认字体  
# matplotlib.rcParams['font.sans-serif']=['SimHei']  
# #设置颜色  
# cm_light=matplotlib.colors.ListedColormap(['#A0FFA0', '#FFA0A0', '#A0A0FF'])  
# cm_dark=matplotlib.colors.ListedColormap(['g','r','b'] )  
  
# grid_hat = classifier.predict(grid_test)       # 预测分类值  
# grid_hat = grid_hat.reshape(x1.shape)  # 使之与输入的形状相同  
  
# plt.pcolormesh(x1, x2, grid_hat, cmap=cm_light)     # 预测值的显示  
# plt.scatter(x[:, 0], x[:, 1], c=y[:,0], s=30,cmap=cm_dark)  # 样本  
# plt.scatter(test_data[:,0],test_data[:,1], c=test_label[:,0],s=30,edgecolors='k', zorder=2,cmap=cm_dark) #圈中测试集样本点  
# plt.xlabel('花萼长度', fontsize=13)  
# plt.ylabel('花萼宽度', fontsize=13)  
# plt.xlim(x1_min,x1_max)  
# plt.ylim(x2_min,x2_max)  
# plt.title('鸢尾花SVM二特征分类')  
# plt.show()