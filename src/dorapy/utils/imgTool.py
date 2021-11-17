'''
img tools
包含图片处理常见工具.
function:
1. 根据路径返回img
2. 根据路径保存图片
3. 画折线图
4. 切割图片
'''
import sys
sys.path.append(r'./')      # 为了能找到自写函数

import cv2
import numpy as np

'''
根据路径返回img
get_img(getpath, gray=False, scale_percent=100)
getpath:图片路径
gray:是否显示为灰度图;default=False
scale_percent:放缩比例;default=100
'''
def get_img(getpath, gray=False, scale_percent=100):
    img = cv2.imread(getpath)

    if gray:img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)		# 转换为灰度图  解决cv读取灰度图成为三通道的问题
    
    if scale_percent != 100:
        # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    return img

# 保存图片
def save_img(savepath, img):
    cv2.imwrite(savepath, img)


# 画折线图
def plot_line_chart(y1, y2, y3):
    
    import matplotlib.pyplot as plt     # 其他函数用不到,这个也不会频繁调用，就放这里了
    plt.figure(figsize=(20,2))
    plt.title('太阳风速度预测')  # 折线图标题
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示汉字
    plt.xlabel('time')  # x轴标题
    plt.ylabel('太阳风速 km/s')  # y轴标题
    plt.plot(y1, color='#800080', label='true', linewidth=1)  # 绘制折线图，添加数据点，设置点的大小
    # plt.plot(y2, color='#00a8e1', label='p1', linewidth=1)
    plt.plot(y3, color='#99cc00', label='p2', linewidth=1)

    plt.legend(['True', 'P2'])  # 设置折线名称
    # plt.legend(['True', 'P1', 'P2'])  # 设置折线名称
    plt.show()  # 显示折线图

# 切割图片
def cut_pic(img,pattern=0, up = 0, down = 0, left = 0, right = 0):
    '''
    (img, 切割模式(0:比例,1:像素),图片上部分, 图片下, 左, 右)\n
    eg.\n
    >>>(img, 1, 50, 50, 50, 50)\n
    上下左右各切50像素\n
    >>>(img, 0, 0.2, 0.2, 0.2, 0.2)\n
    上下左右各切20%\n
    '''
    h, w = len(img), len(img[0])
    if pattern:
        img = img[up:h - down, left:w-right]
    else:
        img = img[int(h*up):int(h*(1-down)), int(w*left):int(w*(1-right))]
    return img





if __name__ == '__main__':
    print("Welcome to MyTools!")
    from utils.txtTool import *
    # l1 = txtReadNumArray("./example/data/true.txt")
    # l2 = txtReadNumArray("./example/data/p1.txt")
    # l3 = txtReadNumArray("./example/data/p2.txt")
    # plot_line_chart(l1[120:8000],l2[0:8000],l3[0:8000])
    imgpath = "./example/test.jpg"
    img = get_img(imgpath, gray=True, scale_percent=25)
    # img = img[50:462, 50:462]
    # img = cut_pic(img, 1, 50, 50, 50, 50)
    img = cut_pic(img, 1, 14, 14, 14, 14)

    img = 255.-img
 
    from mathTool import *
    img = standardization(img)
    # print(img[0:5,0:5])
    # print(img[40:50,40:50])
    print(np.array(img).shape)

    from circle import *
    box = box_circle(100, (49,49), 50, 0., 1.)
    img = img*box
    
    print(img[0:5,0:5])
    print(img[40:50,40:50])
    cv2.imshow("img", img)

    cv2.waitKey (0)  
    cv2.destroyAllWindows()

