#!/user/bin/env python3
#!-*- coding:utf-8 -*-
'''
Created on 2018年4月1日17:31:58

@author: RecluseXu
'''

import cv2 as cv
import cv2 as zzz
import numpy as np
from collections import Counter
from math import sqrt


def template_demo(target,tpl): # openCV模板匹配
    # 目标图与匹配图
    # 返回最适合匹配的正方形的 左上角和右下角 坐标
    methods = [cv.TM_SQDIFF_NORMED,cv.TM_CCORR_NORMED,cv.TM_CCOEFF_NORMED]
    target_h,target_w = tpl.shape[:2]
    
    br_list = []
    tl_list = []
    for method in methods:
        result = cv.matchTemplate(target,tpl,method)
        min_val,max_val,min_loc,max_loc = cv.minMaxLoc(result)
        if(method == cv.TM_SQDIFF_NORMED):
            tl = min_loc
        else:
            tl = max_loc
        br = (tl[0]+target_w, tl[1]+target_h)
        tl_list.append(tl)
        br_list.append(br)
#         cv.rectangle(target,tl,br,(0,0,255),2)
#         cv.imshow('match',target)
#         cv.imwrite('picture/match-'+np.str(method)+'.png',target)
#         cv.imshow('methodResult',result)
#         cv.imwrite('picture/methodResult-'+np.str(method)+'.png',target)
    
    tl = Counter(tl_list).most_common(1)[0][0] # 左上
    br = Counter(br_list).most_common(1)[0][0] # 右下
    
    return [tl,br]

def find_next_flat_top(screenshot): # 找下一个平台平台最上点
    screenshot_gray = cv.cvtColor(screenshot, cv.COLOR_RGB2GRAY) # 灰度
    rows, cols = screenshot_gray.shape[:2]
    # 先把最上面1/4屏幕高度的东西删掉
    screenshot_gray_cut = screenshot_gray[int(rows/4):] 
    # 每一行像素     最大值-最小值 ，得到最大差值组
    screenshot_gray_cows_maxmin = screenshot_gray_cut.max(axis=1)-screenshot_gray_cut.min(axis=1)
    # 从上到下扫描，找到第一个有差值的地方，那就是下一个平台最上点
    for row in range(0,screenshot_gray_cows_maxmin.shape[0]):
        if(screenshot_gray_cows_maxmin[row] > 20):
            flat_top_y = row + int(rows/4) # 下一个平面最高点y坐标,这里把原本删了的1/4屏幕高度补回来
            break
    
    flattop_cow = screenshot_gray[flat_top_y] # 将下一个平面最高点所在行拿出来
    more = np.argmax(np.bincount(flattop_cow)) # 算众数
    notelist = [] # 记录不同点的x坐标
    for x in range(0, flattop_cow.shape[0]):
        if(flattop_cow[x] == more): # 是众数，不管
            continue
        else:
            if(len(notelist) == 0): # 记录表为空
                notelist.append(x) # 直接加
            else:
                for item in notelist: # 如果这个像素不是孤立的，加进去
                    if(item == x-1):
                        notelist.append(x)
    flat_top_x = int(sum(notelist)/len(notelist))# 取 不同点x坐标记录的平均数 作为 下一个平面最高点x坐标
    return (flat_top_x,flat_top_y)

def find_next_flat_beside(screenshot, underchess_center_location, next_plat_top): # 找到下一个平台 靠近边缘的点
    rows, cols = screenshot.shape[:2] # 获取 高与宽 
    aim_point = screenshot[next_plat_top[1]+2][next_plat_top[0]] # 获取最高点的像素信息
    
    # 算算，棋子是在左边还是在右边，以便判断边角在哪边。
    if(underchess_center_location[0] > cols/2): # 判断棋子在 屏幕左边 还是 右边
        # 棋子在右边
        parm1 = 0
        parm2 = underchess_center_location[0]
        parm3 = 1
    else: # 棋子在左边
        parm1 = cols-1
        parm2 = underchess_center_location[0]
        parm3 = -1
    find = False
    for col in range(parm1, parm2, parm3): # 根据参数调整扫描方式
        for row in range(next_plat_top[0], underchess_center_location[1]):# 从上往下
            equ = np.array_equal(aim_point, screenshot[row][col])
            if(equ):
                beside = (col,row)
                find = True
                break
        if(find):
            break
    return beside

def count_distance(underchess_center_location, next_plat_center): # 计算有多远
    det_x_2 = (underchess_center_location[0]-next_plat_center[0])*(underchess_center_location[0]-next_plat_center[0])
    det_y_2 = (underchess_center_location[1]-next_plat_center[1])*(underchess_center_location[1]-next_plat_center[1])
    distance = sqrt(det_x_2+det_y_2)
    return distance

def process(picture_location='picture/'):
#     cv.namedWindow('inputImage',cv.WINDOW_AUTOSIZE)
    screenshot_img = cv.imread(picture_location + 'screenshot.png')
    chessbody_img = cv.imread(picture_location + 'chess_body.png')
    
    # 通过openCV模式匹配找到棋身
    chessbody_edge_location = template_demo(screenshot_img, chessbody_img)
    # 通过棋身的左上和右下的坐标得到棋底的中间坐标位置
    underchess_center_location = (int((chessbody_edge_location[0][0]+chessbody_edge_location[1][0])/2), int((chessbody_edge_location[0][1]+chessbody_edge_location[1][1])/2)+30)
    # 找到下一个平台最高点坐标
    next_plat_top = find_next_flat_top(screenshot_img) # 计算下一个平面最高点
#     find_next_plant(screenshot_img, underchess_center_location)
    # 计算下一个平台的边缘坐标
    next_plat_beside = find_next_flat_beside(screenshot_img, underchess_center_location, next_plat_top) # 计算下一个平台的边缘点
    # 下一个平台的中心坐标
    next_plat_center = (next_plat_top[0],next_plat_beside[1])
    
    # 画
    cv.rectangle(screenshot_img, chessbody_edge_location[0],chessbody_edge_location[1],(0,0,255),1) # 画出棋身
    cv.circle(screenshot_img, underchess_center_location, 5, (0,0,255), -1) # 画出棋底标记位置
    cv.circle(screenshot_img, next_plat_top, 5, (0,0,255), -1) # 画出下一个平台最高点坐标
    cv.circle(screenshot_img, next_plat_beside, 5, (0,0,255), -1) # 画出下一个平台的边缘坐标
    cv.circle(screenshot_img, next_plat_center, 5, (0,0,255), -1) # 画出棋下一个平台的中心
    cv.line(screenshot_img, underchess_center_location, next_plat_center, (255, 0, 255), 5)
#     cv.imwrite('picture/draw.png', screenshot_img)
#     cv.imshow('inputImage',cv.pyrDown(screenshot_img))
    
#     cv.waitKey(0)
#     cv.destroyAllWindows()
    return count_distance(underchess_center_location, next_plat_center)

if __name__ == '__main__':
    process()
