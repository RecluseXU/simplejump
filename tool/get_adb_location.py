#!/user/bin/env python3
#!-*- coding:utf-8 -*-
'''
Created on 2018年4月1日12:39:45
    这东西其实就是获取adb路径的
@author: RecluseXu
'''

import sys

def get_running_file_location(): # 获取当前运行的python程序文件的路径。
    return str(sys.argv[0])

def get_adb_location(): # 获取adb路径的
    running_file_location = get_running_file_location() # 获取当前运行py文件路径
    project_location = running_file_location[:running_file_location.find('\\simplejump\\') + len('\\simplejump\\')]
    adb_location = project_location + 'tool\\adb\\'
    return adb_location

def get_picture_location(): # 获取图片文件夹路径
    running_file_location = get_running_file_location() # 获取当前运行py文件路径
    project_location = running_file_location[:running_file_location.find('\\simplejump\\') + len('\\simplejump\\')]
    adb_location = project_location + 'tool\\picture\\'
    return adb_location
if __name__ == '__main__':
    print(get_adb_location())