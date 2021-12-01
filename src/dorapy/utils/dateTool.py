'''
获取当前时间方便文件命名

function:
1. getDateYMDHMSU()     返回年月日|时分秒|毫秒
2. getDateYMD()         返回年月日
3. getDateYMDHMS()      返回年月日|时分秒

'''
import datetime


# 返回 年月日 时分秒 毫秒
def getDateYMDHMSU():
    '''
    年月日 时分秒 毫秒
    '''
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d_%H%M%S_%U')

# 返回年月日
def getDateYMD():
    '''
    年月日
    '''
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d')

# 返回 年月日 时分秒
def getDateYMDHMS():
    '''
    年月日
    '''
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d_%H%M%S')

if __name__=='__main__':
    print("Welcome to MyTools!")
    
    print(getDateYMDHMSU())
    print(getDateYMD())
