'''
获取文件夹下所有图片的路径
author:pgcai
function：
1. 获取指定文件夹下指定后缀文件/不包含子文件夹
2. 获取指定文件夹下指定后缀文件/不包含子文件夹//文件名需要为number/排序
3. 获取指定文件夹下指定后缀文件/包含子目录
4. 获取指定文件夹下指定后缀文件/包含子目录/文件名需要为number/排序
5. 根据当前时间新建文件夹
'''
import sys
sys.path.append(r'./utils')      # 为了能找到自写函数

import os
import re
from dateTool import *

'''
获取指定文件夹下指定后缀文件,不包含子文件夹
(文件夹路径, 后缀名)
'''
def get_file(file_path, file_end=('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
    '''
    获取指定文件夹下指定后缀文件,不包含子文件夹
    (文件夹路径, 后缀名)
    '''
    filelist = []
    for parent, dirnames, filenames in os.walk(file_path):
        for filename in filenames:
            if filename.lower().endswith(file_end):
                filelist.append(os.path.join(parent, filename))
        return filelist

'''
获取指定文件夹下指定后缀文件,不包含子文件夹     数字文件排序
(文件夹路径, 后缀名)
'''
def get_numfile(file_path, file_end=('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
    '''
    获取指定文件夹下指定后缀文件,不包含子文件夹     数字文件排序
    (文件夹路径, 后缀名)
    '''
    filelist = []
    for parent, dirnames, filenames in os.walk(file_path):
        filenames.sort(key=lambda x:int(x[:-4]))  # 按文件名排序 
        for filename in filenames:
            if filename.lower().endswith(file_end):
                filelist.append(os.path.join(parent, filename))
        return filelist


'''
获取指定文件夹下指定后缀文件 包含子目录
'''

def get_file_sub(file_path, filelist=[], file_end=('.png', '.jpg')):
    print('\r--------正在统计文件夹下指定后缀文件路径信息--------', end="")
    for parent, dirnames, filenames in os.walk(file_path):
        for dirname in dirnames:
            # print(os.path.join(parent, dirname))
            filelist.extend(get_file_sub(os.path.join(parent, dirname), [], file_end=file_end))
            # print(filelist)
        print(filenames)
        for filename in filenames:
            if filename.lower().endswith(file_end):
                # print("----------------------------------")
                # print(os.path.join(parent, filename))
                # print("----------------------------------")
                filelist.append(os.path.join(parent, filename))
        return filelist

'''
获取指定文件夹下指定后缀文件 包含子目录 文件名需要为 number 便于排序
'''
def get_numfile_sub(file_path, filelist=[], file_end=('.png', '.jpg')):
    print('\r--------正在统计文件夹下指定后缀文件路径信息--------', end="")
    for parent, dirnames, filenames in os.walk(file_path):
        dirnames.sort() # 按文件夹名排序
        # print("--------------------------------")
        # print(dirnames)
        # print("--------------------------------")
        for dirname in dirnames:
            # print(os.path.join(parent, dirname))
            filelist.extend(get_numfile_sub(os.path.join(parent, dirname), [], file_end=file_end))
            # print(filelist)
            
        # print("old",filenames)
        filenames.sort(key=lambda x:int(x[:-4]))  # 按文件名排序 
        # print("new",filenames)
        for filename in filenames:
            if filename.lower().endswith(file_end):
                # print("----------------------------------")
                # print(os.path.join(parent, filename))
                # print("----------------------------------")
                filelist.append(os.path.join(parent, filename))
        return filelist

# 根据当前时间(年月日时分秒)新建文件夹
def new_folder(dirpath):
    timeString = getDateYMDHMS()
    makePath = dirpath + '/' + timeString
    folder = os.path.exists(makePath)

    if not folder:
        os.makedirs(makePath)
        print("make dir success!")
        return(makePath)
    else:
        print("folder already exists！")
        return(makePath)



if __name__ == '__main__':
    print("Welcome to MyTools!")

    trainpath='./example'
    # 获取文件夹包含子目录下后缀为.jpg的文件
    dir_list = get_file_sub(trainpath, file_end=('.jpg'))
    print(dir_list)
    print(len(dir_list))

    # 获取文件夹包含子目录下后缀为.jpg、.png的文件
    print(get_file("./img",('png','jpg')))

    # 根据当前时间(年月日时分秒)新建文件夹
    newPath = new_folder("./example")




