'''
方便操作关于列表的操作。
实现些numpy不便使用的操作

function:
1. 返回你想要的列/一列一个列表
2. 返回你想要的列/一行一个列表
3. 多个npy合并为一个npy文件/输入文件地址/纵向合并 (!文件太大会存不了)
4. 根据路径读取多个npy文件,返回他们纵向合并的列表
'''
import sys
sys.path.append(r'./')      # 为了能找到自写函数



import numpy as np
# from txtTool import *

'''
一些较为基础的函数，重新调用意义不大
np.save(path,arr)
存：save()　　取：load()
'''

# 1. 返回你想要的列/一列一个列表
# alist为原列表, colname为你想要的列的列表，默认为0
def get_iwant_col_y(alist=[["!!!原列表为空"]], colname=[0]):
    alist = np.array(alist)
    blist = []
    for i in colname:
        blist.append(alist[:,i])
    return blist

# 2. 返回你想要的列/一行一个列表
# alist为原列表, colname为你想要的列的列表，默认为0
def get_iwant_col_x(alist=[["!!!原列表为空"]], colname=[0]):
    alist = np.array(alist)
    blist = []
    for i in range(len(alist)):     
        onelist = []
        # print(i)
        for j in colname:
            onelist.append(alist[i, j])
        blist.append(onelist)
    # print(blist)
    return blist


# 3. 多个npy合并为一个npy文件/输入文件地址/纵向合并 (!文件太大会存不了)
'''
a = [[1,2,3],[4,5,6]]
b = [[1,1,1],[2,2,2]]

c = [[1,2,3], [4,5,6], [1,1,1], [2,2,2]]
'''
def npy_plus_npy(npypath = [], tofilepath = ''):
    print(npypath[0])
    x = np.load(npypath[0])
    for i in npypath[1:]:
        print(i)
        y = np.load(i)
        print(y.shape)
        x = np.vstack((x, y))
    print(x.shape)
    np.save(tofilepath, x)

# 4. 根据路径读取多个npy文件,返回他们纵向合并的列表
'''
a = [[1,2,3],[4,5,6]]
b = [[1,1,1],[2,2,2]]

c = [[1,2,3], [4,5,6], [1,1,1], [2,2,2]]
'''
def get_all_npy(npypath = []):
    print(npypath[0])
    x = np.load(npypath[0])
    for i in npypath[1:]:
        print(i)
        y = np.load(i)
        # print(y.shape)
        x = np.vstack((x, y))
    print(x.shape)
    return x


    


if __name__=='__main__':
    print("Welcome to MyTools!")
    from utils.txtTool import txt_read_2dim_num
    from utils.dirTool import *
    txtPath3 = "./example/data/2011.txt"
    a = txt_read_2dim_num(txtPath3)
    print(a)
    b = get_iwant_col_y(a, [0,1])
    print(b[0])
