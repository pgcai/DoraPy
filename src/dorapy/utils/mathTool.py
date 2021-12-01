'''
数学公式库，数学方法库
author:pgcai

function:
1. sigmoid(x)   sigmoid
2. tanh(x)      tanh
3. relu(x)      relu
4. prelu(x, a=0.25)     prelu
5. mean(nlist)  求数组均值
6. var(nlist)   求数组方差
7. std(nlist)   求数组标准差
7. normalization(nlist)     归一化
8. standardization(nlist)   标准化
9. sta_mean_std(nlist, mean, std)   指定 均值 标准差 标准化
10. euclidean_distance(a, b)        计算两向量的欧氏距离
11. vectorial_resultant(a, b)       计算ab两向量合向量
12. vector_angle(a, b)  计算点a指向点b的矢量 且各维度平方和为1
13. linear_equation_in_2unknowns(a, b, c)   解二元一次方程
14. arctan(theta)   输入正切值，返回角度值
15. arcsin(theta)   输入正弦值，返回角度值
16. arccos(theta)   输入余弦值，返回角度值
17. arc_sin_cos(sin_theta, cos_theta)   同时输入sin 与 cos 计算角度值
18. theta_angle(sin_theta, cos_theta, angle)    输入正弦余弦值，返回旋转angle角度后的正弦余弦值
19. vector_3d_angle(v1, v2)     求两个3-dim向量的夹角
20. 
21. 
22. 
23. 
24. 

'''
import math
import numpy as np

# sigmoid
def sigmoid(x):
    return 1./(1 + np.exp(-x))


# tanh
def tanh(x):
    return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))

# relu
def relu(x):
    return 0 if x<=0 else x

# prelu
def prelu(x, a=0.25):
    return x if x>0 else a*x

def mean(nlist):
    # nlist = np.array(nlist).flatten()
    return np.mean(nlist)

# 方差
def var(nlist):
    return np.var(nlist)

# 标准差
def std(nlist):
    return np.std(nlist)

# 归一化
def normalization(nlist):
    min = np.min(nlist)
    numrange = np.max(nlist) - min
    return (nlist - min) / numrange


# 标准化
def standardization(nlist):
    return (nlist - mean(nlist)) / std(nlist)

# 指定 均值 标准差 标准化
def sta_mean_std(nlist, mean, std):
    return (nlist - mean) / std


def euclidean_distance(a, b):
    '''
    计算两向量的欧氏距离
    '''
    if len(a)!=len(b):
        print("please input matrix a, b and len(a)==len(b)")
    vector1 = np.mat(a)
    vector2 = np.mat(b)
    # print (np.sqrt((vector1-vector2)*(vector1-vector2).T))
    return np.asarray(np.sqrt((vector1-vector2)*(vector1-vector2).T))[0][0]


def vectorial_resultant(a, b):
    '''
    计算ab两向量合向量
    '''
    return np.array(b)+np.array(a)


def vector_angle(a, b):
    '''
    计算点位a指向点位b的矢量\n
    且各维度平方和为1
    '''
    c = np.array(b) - np.array(a)
    return c/np.sqrt(np.sum(c*c))

def linear_equation_in_2unknowns(a, b, c):
    '''
    解二元一次方程
    '''
    gen = np.sqrt(b*b - 4*a*c)
    x1 = (-b + gen)/(2.*a)
    x2 = (-b - gen)/(2.*a)
    print(x1, x2)
    return [x1, x2]

def arctan(theta):
    '''
    输入正切值，返回角度值
    '''
    return 180.*math.atan(theta)/math.pi     # 返回角度值

def arcsin(theta):
    '''
    输入正弦值，返回角度值
    '''
    return 180.*math.asin(theta)/math.pi     # 返回角度值

def arccos(theta):
    '''
    输入余弦值，返回角度值
    '''
    return 180.*math.acos(theta)/math.pi     # 返回角度值

def arc_sin_cos(sin_theta, cos_theta):
    '''
    (y,x)
    同时输入sin 与 cos 计算角度值
    '''
    if sin_theta > 0:
        return arccos(cos_theta)
    else:
        return -arccos(cos_theta)

def theta_angle(sin_theta, cos_theta, angle):
    '''
    输入正弦余弦值，返回旋转angle角度后的正弦余弦值
    '''
    _angle = arc_sin_cos(sin_theta, cos_theta)
    angle_now = _angle + angle
    sin_theta2 = math.sin(math.pi*angle_now/180)
    cos_theta2 = math.cos(math.pi*angle_now/180)
    return sin_theta2, cos_theta2

def vector_3d_angle(v1, v2):
    '''
    求两个3-dim向量的夹角
    '''
    v1 = np.array(v1)
    v2 = np.array(v2)
    # print('np.sum(v1*v2) = ', np.sum(v1*v2))
    # print('np.sqrt(np.sum(v1*v1)) = ', np.sqrt(np.sum(v1*v1)))
    # print('np.sqrt(np.sum(v2*v2)) = ', np.sqrt(np.sum(v2*v2)))
    cos_theta = np.sum(v1*v2)/(np.sqrt(np.sum(v1*v1))*np.sqrt(np.sum(v2*v2)))
    print(cos_theta)
    return arccos(cos_theta)

if __name__=='__main__':
    # print(str(relu(-1)))
    # print(str(relu(999)))
    # a = [4, 2, 35, 4, 325, 6, 1, 345, 54, 4, 554, 6, 1, 325, 78, 4, 55, 676]
    # print(mean(a))
    # print(var(a))
    # print(std(a))
    # b = [[[4, 2], [35, 4], [325,6]],
    # [[1, 345], [54, 4], [554,6]],
    # [[1, 325], [78, 4], [55,676]]]
    # print(mean(b))
    # print(var(b))
    # print(std(b))

    # print(standardization(a))
    # print(standardization(b))

    # x = [1,2,3,1,2,3,1,2,3,1,2,3]
    # y = [10,23,35,11,24,23,41,12,34,1237,72,53]
    # print(euclidean_distance(x,y))

    # print(vectorial_resultant(x, y))

    # linear_equation_in_2unknowns(4.9, 1000, -999)

    tan_theta = math.sqrt(3.)/3.
    sin_theta = 0.5
    cos_theta = math.sqrt(3.)/2.
    print(arctan(tan_theta))
    print(arcsin(-sin_theta))
    print(arccos(cos_theta))
    print(arccos(-cos_theta))

    print(arc_sin_cos(sin_theta, cos_theta))
    print(arc_sin_cos(sin_theta, -cos_theta))
    print(arc_sin_cos(-sin_theta, -cos_theta))
    print(arc_sin_cos(-sin_theta, cos_theta))

    theta2 = 100
    sin_theta2 = math.sin(math.pi*theta2/180)
    cos_theta2 = math.cos(math.pi*theta2/180)

    print(arc_sin_cos(sin_theta2, cos_theta2))

    sin_theta3, cos_theta3 = theta_angle(sin_theta2, cos_theta2, 30)

    print(arc_sin_cos(sin_theta3, cos_theta3))

    print(vector_3d_angle([1,1,0], [1,-1,0]))
    



