'''
操作txt文件的工具箱
author:pgcai

function:
1. check_dir(file_path)     检查文件地址的合法性,不存在文件夹则新建
2. txtRead(file_path)       打开txt文件并返回全部内容
3. txtReadArray(file_path)  以列表形式返回txt中的内容 去掉回车‘\n’
4. txtReadNumArray(file_path, tList=[])     以列表形式返回txt中的内容 去掉回车‘\n’ 并将他们都转化为float类型
5. txt_read_2dim(file_path, tList=[])       以列表形式返回txt中的内容(有字符串)/并去掉回车‘\n’/每一行有多个属性
6. txt_read_2dim_num(file_path, tList=[])   以列表形式返回txt中的内容(纯数字，提前转换为浮点型)/并去掉回车‘\n’/每一行有多个属性
7. txtWrite(file_path, str) 对txt文件写入字符串 str
8. txtAddWrite(file_path, str)          对txt文件!!增添写入字符串 str
9. txtWriteArray(file_path, tList=[])   “新建”txt文件写入一个数组 "一个元素一行"
10. txtAddWriteArray(file_path, tList=[])   “对原有”txt文件写入一个数组 "一个元素一行"
11. txtAddtxt(path1, path2)     两个txt文件 拼接
12. txt_write_2d_array(file_path, tList=[[]])   “新建”txt文件写入一个2-dim列表/"多个属性一行"
13. 
14. 
15. 
16. 




模式    可做操作    若文件不存在    是否覆盖
r       只能读         报错         -
r+      可读可写        报错        是
w       只能写          创建        是
w+      可读可写        创建        是
a       只能写          创建        否，追加写
a+      可读可写        创建        否，追加写
'''
import os


def check_dir(file_path):
    '''
    检查文件地址的合法性,不存在文件夹则新建
    '''
    # 检查路径合法性
    index = -1
    for i in file_path[::-1]:
        if i == '/' or i == '\\':
            break
        else:
            index-=1
    dirpath = file_path[:index]
    # print(dirpath)
    folder = os.path.exists(dirpath)
    if not folder:
        os.makedirs(dirpath)


'''
读取
'''

def txtRead(file_path):
    '''
    打开txt文件并返回全部内容
    '''
    with open(file_path,"r") as f:  #设置文件对象
        str = f.read()     #将txt文件的所有内容读入到字符串str中
    return str

def txtReadArray(file_path):
    '''
    以列表形式返回txt中的内容 去掉回车‘\n’
    '''
    tList=[]
    with open(file_path,'r') as f:    #设置文件对象
        tList = f.readlines()
    tList = [i[:-1] for i in tList]
    return tList

def txtReadNumArray(file_path, tList=[]):
    '''
    以列表形式返回txt中的内容 去掉回车‘\n’ 并将他们都转化为float类型
    '''
    with open(file_path,'r') as f:    #设置文件对象
        tList = f.readlines()
    tList = [float(i[:-1]) for i in tList]
    return tList

def txt_read_2dim(file_path, tList=[]):
    '''
    以列表形式返回txt中的内容(有字符串)/并去掉回车‘\n’/每一行有多个属性
    '''
    f = open(file_path)               # 返回一个文件对象   
    line = f.readline()               # 调用文件的 readline()方法   
    while line:
        tList.append(line[:-1].split())        # 不指定时 默认空格  有多个空格能跳过
        line = f.readline()   
    f.close()
    return tList

def txt_read_2dim_num(file_path, tList=[]):
    '''
    以列表形式返回txt中的内容(纯数字，提前转换为浮点型)/并去掉回车‘\n’/每一行有多个属性
    '''
    f = open(file_path)               # 返回一个文件对象   
    line = f.readline()               # 调用文件的 readline()方法   
    while line: 
        alist = line[:-1].split()
        new = []
        for i in alist:
            new.append(float(i))
        tList.append(new)        # 不指定时 默认空格  有多个空格能跳过
        line = f.readline()   
    f.close()
    return tList

'''
写入
'''
def txtWrite(file_path, str):
    '''
    对txt文件写入字符串 str
    '''
    with open(file_path,'w') as f:    #设置文件对象
        f.write(str)        #将字符串写入文件中


def txtAddWrite(file_path, str):
    '''
    对txt文件!!增添写入字符串 str
    '''
    with open(file_path,'a') as f:    #设置文件对象
        f.write(str+'\n')        #将字符串写入文件中


def txtWriteArray(file_path, tList=[]):
    '''
    “新建”txt文件写入一个数组 "一个元素一行"
    '''
    check_dir(file_path)    # 检查文件夹路径的合法性

    tList = [str(i)+"\n" for i in tList]
    with open(file_path,'w') as f:    #设置文件对象
        f.writelines(tList)
    print("txt ok!")


def txtAddWriteArray(file_path, tList=[]):
    '''
    “对原有”txt文件写入一个数组 "一个元素一行"
    '''
    tList = [str(i) + "\n" for i in tList]
    with open(file_path,'a') as f:    #设置文件对象
        f.writelines(tList)

def txtAddtxt(path1, path2):
    '''
    两个txt文件 拼接
    '''
    list2 = txtReadArray(path2)
    txtAddWriteArray(path1, list2)

def txt_write_2d_array(file_path, tList=[[]]):
    '''
    “新建”txt文件写入一个2-dim列表/"多个属性一行"
    '''

    check_dir(file_path)    # 检查文件夹路径的合法性

    # tList = [str(i)+"\n" for i in tList]
    with open(file_path,'w') as f:    #设置文件对象
        for i in range(len(tList[0])):
            aline = ''
            for j in range(len(tList)):
                aline = aline + ' ' + str(tList[j][i])
            aline += '\n'
            f.writelines(aline)
    print("txt ok!")


if __name__ == '__main__':
    print("Welcome to MyTools!")
    txtPath = "./example/data/test.txt"
    txtPath2 = "./example/data/test2.txt"
    txtPath3 = "./example/data/2011.txt"
    txtAddWrite(txtPath,"95633")
    # txtWriteArray(txtPath,[1212, 452345, 2135123])
    txtWriteArray(txtPath,[1, 2, 3])
    txtWriteArray(txtPath2,[4, 5, 6])
    print(len(txtReadArray(txtPath2)))
    print(txtRead(txtPath))
    
    txtAddtxt(txtPath, txtPath2)

    a = txt_read_2dim(txtPath3)
    print(a)






