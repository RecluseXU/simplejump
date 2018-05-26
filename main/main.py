#!/user/bin/env python3
#!-*- coding:utf-8 -*-
'''
Created on 2018年4月2日15:36:46

@author: RecluseXu
'''

from tool.get_adb_location import get_adb_location, get_picture_location
from tool.get_phone_screenshot import Screenshot,screen_process
from tool.image_handle import process

if(__name__=='__main__'):
    adb_location = get_adb_location()
    print('adb路径：',adb_location)
    picture_location = get_picture_location().replace('\\','/')
    print('picture路径：',picture_location)  
    screenshot = Screenshot(adb_location,picture_location) # 实例化一个Screenshot对象
    
    z='q'

    while(z!='z'):
        screen_process(screenshot) # 丢进函数获取截屏到项目中
        distance = process(picture_location) # 运行这个东西进行分析
        screenshot.operation_5(int(distance))
#         z = input()
    screenshot.operation_4()
    