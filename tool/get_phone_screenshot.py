#!/user/bin/env python3
#!-*- coding:utf-8 -*-
'''
Created on 2018年4月1日12:23:47
    这个东西只提供一个screen_process(adb_location)方法
    adb_location ：项目中adb执行文件的路径
@author: RecluseXu
'''
import subprocess
import os
from tool.get_adb_location import get_adb_location,get_picture_location
import random


class Screenshot():#截取手机屏幕并保存到电脑  
    def __init__(self,adb_location,picture_location):
        # 保存adb路径到类中，以便等下执行命令使用
        self.adb_location = adb_location
        self.picture_location = picture_location
        #查看连接的手机
        print('连接手机')
        connect = subprocess.Popen(self.adb_location + "adb devices", stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)  
        stdout,stderr = connect.communicate()   #获取返回命令  
        # 输出执行命令结果结果  
        stdout = stdout.decode("GBK").replace('\n','')
        stderr = stderr.decode("GBK").replace('\n','') 
        print(stdout, end='')  
        print(stderr, end='')
    def adb_commander(self,cmd):
        screenExecute = subprocess.Popen(str(cmd), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)  
        stdout, stderr = screenExecute.communicate()  
        # 输出执行命令结果结果  
#         stdout = stdout.decode("GBK").replace('\n','')
#         stderr = stderr.decode("GBK").replace('\n','')
#         print(stdout, end='')
#         print(stderr, end='')
        
    def operation_1(self): # 命令1：将项目中的已经存在的截屏图片删除。
        print('\t删除电脑中上次保存的截屏图片......', end='')
        if os.path.exists(self.picture_location + 'screenshot.png'):
            #删除文件，可使用以下两种方法。
            print('删除图片', end='')
            os.remove(self.picture_location + 'screenshot.png')
            #os.unlink(my_file)
            print('......成功')
        else:
            print('未找到截屏图片')
        
    def operation_2(self,fi=True): # 命令2：在手机上截屏，保存为到/sdcard/screenshot.png
        cmd = self.adb_location + r"adb shell /system/bin/screencap -p /sdcard/screenshot.png"
        if(fi):
            print('\t手机截屏', end='')
        self.adb_commander(cmd)
        if(fi):
            print('......成功')
        
    def operation_3(self,fi=True): # 命令3：将/sdcard/screenshot.png传输到项目screenshot/screenshot.png中
        cmd = self.adb_location + r"adb pull /sdcard/screenshot.png "+self.picture_location+"screenshot.png"
        if(fi):
            print('\t手机截屏传到电脑', end='')
        self.adb_commander(cmd)
        while(os.path.exists(self.picture_location + 'screenshot.png') != True): # 再次尝试
            print('......失败\n\t再次尝试',end='')
            self.operation_2(fi=False)
            self.operation_3(fi=False)
        if(fi):
            print('......成功')
            
    def operation_4(self): # 命令4：删除手机中的截屏图片
        cmd = self.adb_location + r"adb shell rm /sdcard/screenshot.png"
        print('\t删除手机中的截屏图片', end='')
        self.adb_commander(cmd)
        print('......成功')
    def operation_5(self,distance):
        press_time = int(distance * 1.4)
        # 生成随机手机屏幕模拟触摸点
        # 模拟触摸点如果每次都是同一位置，成绩上传可能无法通过验证
        rand = random.randint(0, 9) * 10
        cmd = self.adb_location + 'adb shell input swipe %i %i %i %i ' % (320 + rand, 410 + rand, 320 + rand, 410 + rand)
        cmd = cmd + str(press_time)
        print('\t发送点击命令', end='')
        self.adb_commander(cmd)
        print('......成功')
        
def screen_process(screenshot_example):
    # 逐步执行
    print('获取截屏')
    screenshot_example.operation_1()
    screenshot_example.operation_2()
    screenshot_example.operation_3()
#     screenshot_example.operation_4() # 为了提高效率，我将它移动到了main那里，退出的时候才执行
    
if __name__ == '__main__':
    adb_location = get_adb_location()
    print('adb路径：',adb_location)
    picture_location = get_picture_location().replace('\\','/')
    print('picture路径：',picture_location)
    screenshot = Screenshot(adb_location,picture_location) # 实例化一个Screenshot对象
    screen_process(screenshot) # 丢进函数自动走一遍流程
    
    
    
