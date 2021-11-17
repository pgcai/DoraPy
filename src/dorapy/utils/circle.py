'''
function:
1. 生成图案/方形中间为圆/圆value=y边value=x的box
'''
import numpy as np
from skimage import draw, data


def box_circle(box_length, center, radius, x, y): 
    '''
    生成方形中间为圆，圆value=y 边value=x 的box\n
    (方长, 圆形位置, 半径, 方值, 圆值)
    '''
    box = np.full((box_length, box_length), x)
    rr, cc=draw.disk(center,radius)
    box[rr, cc] = y
    # print(box.sum())
    return box

if __name__=='__main__':
    print("Welcome to MyTools!")