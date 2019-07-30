# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np

# 汽车计数
car_num = len(os.listdir(os.path.join('data', 'car')))


def preprocess(gray):
    # # 直方图均衡化
    # equ = cv2.equalizeHist(gray)
    # 高斯平滑
    gaussian = cv2.GaussianBlur(gray, (3, 3), 0, 0, cv2.BORDER_DEFAULT)
    # 中值滤波
    median = cv2.medianBlur(gaussian, 5)
    # Sobel算子，X方向求梯度
    sobel = cv2.Sobel(median, cv2.CV_8U, 1, 0, ksize=3)
    # 二值化
    ret, binary = cv2.threshold(sobel, 170, 255, cv2.THRESH_BINARY)
    # 膨胀和腐蚀操作的核函数
    element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
    element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 7))
    # 膨胀一次，让轮廓突出
    dilation = cv2.dilate(binary, element2, iterations=1)
    # 腐蚀一次，去掉细节
    erosion = cv2.erode(dilation, element1, iterations=1)
    # 再次膨胀，让轮廓明显一些
    dilation2 = cv2.dilate(erosion, element2, iterations=3)
    # cv2.imshow('dilation2', dilation2)
    # cv2.waitKey(0)
    return dilation2


def findPlateNumberRegion(img):
    region = []
    # 查找轮廓
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # list_rate = []
    # 筛选面积小的
    for i in range(len(contours)):
        cnt = contours[i]
        # 计算该轮廓的面积
        area = cv2.contourArea(cnt)

        # 面积小的都筛选掉
        if area < 900:
            continue

        # 找到最小的矩形，该矩形可能有方向
        rect = cv2.minAreaRect(cnt)
        print("rect is:", rect)

        # box是四个点的坐标
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        # 计算高和宽
        height = abs(box[0][1] - box[2][1])
        width = abs(box[0][0] - box[2][0])
        # 车牌正常情况下长高比在2.7-5之间
        ratio = float(width) / float(height)
        print(ratio)
        if ratio > 5 or ratio < 2:
            continue
        # x, y, w, h
        region.append([*box[2], width, height])
    return region


def car_brand_detect(img):
    global car_num
    if img is None:
        print('Input Error!! 请输入正确路径')
        return []

    # 保存图片
    cv2.imwrite(os.path.join('data', 'car', str(car_num)+'.jpg'), img)
    car_num += 1
    # 转化成灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 形态学变换的预处理
    dilation = preprocess(gray)

    # 查找车牌区域
    region = findPlateNumberRegion(dilation)

    return region


