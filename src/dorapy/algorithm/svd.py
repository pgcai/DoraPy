'''
奇异值分解
Singular Value Decomposition
author:pgcai
20211201

输入：样本数据
输出：左奇异矩阵，奇异值矩阵，右奇异矩阵
计算特征值： 特征值分解AAT，其中A∈Rm×n为原始样本数据

AAT=UΣΣTUT
得到左奇异矩阵U∈Rm×m和奇异值矩阵Σ′∈Rm×m

间接求部分右奇异矩阵： 求V′∈Rm×n

利用A=UΣ′V′可得

V′=(UΣ′)−1A=(Σ′)−1UTA(1-4)
返回U, Σ′, V′，分别为左奇异矩阵，奇异值矩阵，右奇异矩阵。
'''
import numpy as np


def svd(data):
    '''
    Singular Value Decomposition
    '''
    # 数据必需先转为浮点型，否则在计算的过程中会溢出，导致结果不准确
    data2Float = np.array(data, dtype=float)
    # 计算特征值和特征向量
    eval_sigma1, evec_u = np.linalg.eigh(data2Float.dot(data2Float.T))

    # 降序排列后，逆序输出
    eval1_sort_idx = np.argsort(eval_sigma1)[::-1]
    # 将特征值对应的特征向量也对应排好序
    eval_sigma1 = np.sort(eval_sigma1)[::-1]
    evec_u = evec_u[:,eval1_sort_idx]
    # 计算奇异值矩阵的逆
    eval_sigma1 = np.sqrt(eval_sigma1)
    eval_sigma1_inv = np.linalg.inv(np.diag(eval_sigma1))
    # 计算右奇异矩阵
    evec_part_v = eval_sigma1_inv.dot((evec_u.T).dot(data2Float))

    return evec_u, eval_sigma1, evec_part_v




if __name__=='__main__':
    print("svd")
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    img_eg = mpimg.imread("./data/test2.jpg")
    print(img_eg.shape)
    img_temp = img_eg.reshape(img_eg.shape[0], img_eg.shape[1] * img_eg.shape[2])
    # U,Sigma,VT = np.linalg.svd(img_temp)
    U, Sigma, VT = svd(img_temp)


    # 取前60个奇异值
    sval_nums = 60
    img_restruct1 = (U[:,0:sval_nums]).dot(np.diag(Sigma[0:sval_nums])).dot(VT[0:sval_nums,:])
    img_restruct1 = img_restruct1.reshape(img_eg.shape[0], img_eg.shape[1], img_eg.shape[2])


    print(Sigma.shape)
    print('压缩前数据量 = ', img_eg.shape[0] * img_eg.shape[1] * img_eg.shape[2])
    print('压缩后数据量 = ', img_eg.shape[0]*sval_nums + sval_nums + sval_nums*img_eg.shape[1] * img_eg.shape[2])
    
    # 取前120个奇异值
    sval_nums = 120
    img_restruct2 = (U[:,0:sval_nums]).dot(np.diag(Sigma[0:sval_nums])).dot(VT[0:sval_nums,:])
    img_restruct2 = img_restruct2.reshape(img_eg.shape[0], img_eg.shape[1], img_eg.shape[2])


    print(Sigma.shape)
    print('压缩前数据量 = ', img_eg.shape[0] * img_eg.shape[1] * img_eg.shape[2])
    print('压缩后数据量 = ', img_eg.shape[0]*sval_nums + sval_nums + sval_nums*img_eg.shape[1] * img_eg.shape[2])


    fig, ax = plt.subplots(1, 3, figsize = (24,32))
    
    ax[0].imshow(img_eg)
    ax[0].set(title = "src")
    ax[1].imshow(img_restruct1.astype(np.uint8))
    ax[1].set(title = "nums of sigma = 60")
    ax[2].imshow(img_restruct2.astype(np.uint8))
    ax[2].set(title = "nums of sigma = 120")

    plt.show()