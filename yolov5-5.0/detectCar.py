# import cv2
# import numpy as np
#
# # img_path = cv2.imread('./rest/yellow.png')
# # img_path = cv2.imread('./rest/blue.jpg')
# img_path = cv2.imread('C:\\Users\\19409\\Desktop\\data\\yolov5-5.0\\runs\\detect\\exp45\\plates\\bp3sGrn4ov_1.jpg')
# cv2.imshow('origin', img_path)
#
# height = img_path.shape[0]
# width = img_path.shape[1]
# print('面积：', height * width)
#
#
# # 设定阈值
# lower_blue = np.array([100, 43, 46])
# upper_blue = np.array([124, 255, 255])
# lower_yellow = np.array([15, 55, 55])
# upper_yellow = np.array([50, 255, 255])
# lower_green = np.array([0, 3, 116])
# upper_green = np.array([76, 211, 255])
#
# # 转换为HSV
# hsv = cv2.cvtColor(img_path, cv2.COLOR_BGR2HSV)
#
# # 根据阈值构建掩膜
# mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
# mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)  #
# mask_green = cv2.inRange(hsv, lower_green, upper_green)  #
#
# # 对原图像和掩膜进行位运算
# # src1：第一个图像（合并的第一个对象）src2：第二个图像（合并的第二个对象）mask：理解为要合并的规则。
# res_blue = cv2.bitwise_and(img_path, img_path, mask=mask_blue)
# res_yellow = cv2.bitwise_and(img_path, img_path, mask=mask_yellow)
# res_green = cv2.bitwise_and(img_path, img_path, mask=mask_green)
#
# # 显示图像
# # cv2.imshow('frame', img_path)
# cv2.imshow('mask_blue', mask_blue)
# cv2.imshow('mask_yellow', mask_yellow)
# cv2.imshow('mask_green', mask_green)
# # cv2.imshow('res', res)
#
# # 对mask进行操作--黑白像素点统计  因为不同颜色的掩膜面积不一样
# # 记录黑白像素总和
#
# blue_white = 0
# blue_black = 0
# yellow_white = 0
# yellow_black = 0
# green_white = 0
# green_black = 0
#
# # 计算每一列的黑白像素总和
# for i in range(width):
#     for j in range(height):
#         if mask_blue[j][i] == 255:
#             blue_white += 1
#         if mask_blue[j][i] == 0:
#             blue_black += 1
#         if mask_yellow[j][i] == 255:
#             yellow_white += 1
#         if mask_yellow[j][i] == 0:
#             yellow_black += 1
#         if mask_green[j][i] == 255:
#             green_white += 1
#         if mask_green[j][i] == 0:
#             green_black += 1
#
# print('蓝色--白色 = ', blue_white)
# print('蓝色--黑色 = ', blue_black)
# print('黄色--白色 = ', yellow_white)
# print('黄色--黑色 = ', yellow_black)
# print('绿色--白色 = ', green_white)
# print('绿色--黑色 = ', green_black)
#
# color_list = ['蓝色','黄色','绿色']
# num_list = [blue_white,yellow_white,green_white]
#
# print('车牌的颜色为:',color_list[num_list.index(max(num_list))])
#
# cv2.waitKey(0)
#
import cv2

def detect_plate_color(image_path):
    # 读取图像
    image = cv2.imread(image_path)

    # 定义颜色区间的阈值
    lower_yellow = (20, 100, 100)
    upper_yellow = (30, 255, 255)
    lower_blue = (100, 50, 50)
    upper_blue = (140, 255, 255)
    lower_green = (40, 50, 50)
    upper_green = (80, 255, 255)

    # 将图像转换为HSV颜色空间
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 通过颜色阈值来提取颜色区域
    yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
    blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # 统计各个颜色区域的像素数量
    yellow_pixels = cv2.countNonZero(yellow_mask)
    blue_pixels = cv2.countNonZero(blue_mask)
    green_pixels = cv2.countNonZero(green_mask)

    # 根据像素数量判断车牌颜色
    if yellow_pixels > blue_pixels and yellow_pixels > green_pixels:
        return "/*黄色*/"
    elif blue_pixels > yellow_pixels and blue_pixels > green_pixels:
        return "/*蓝色*/"
    elif green_pixels > yellow_pixels and green_pixels > blue_pixels:
        return "/*绿色*/"
    else:
        return "/*无法识别*/"

# 测试
# image_path = "C:\\Users\\19409\\Desktop\\data\\yolov5-5.0\\runs\\detect\\exp41\\plates\\7qqVL3Ksej_1.jpg"  # 替换为你的图像路径
# plate_color = detect_plate_color(image_path)
# print("Plate color:", plate_color)

