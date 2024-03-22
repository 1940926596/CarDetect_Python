import cv2
# import matplotlib.pyplot as plt
import numpy as np


# 定义一个展示图片的函数
def cv_show(name, img):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 定义一个形态学处理的函数
def good_thresh_img(img):
    gs_frame = cv2.GaussianBlur(img, (5, 5), 0)  # 高斯滤波
    hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)  # 转化成HSV图像
    erode_hsv = cv2.erode(hsv, None, iterations=2)
    return erode_hsv


# 定义一个识别目标颜色并处理的函数
def select_color_img(target_color, img):
    for i in target_color:
        mask = cv2.inRange(erode_hsv, color_dist[i]['Lower'], color_dist[i]['Upper'])
        if (i == target_color[0]):
            inRange_hsv = cv2.bitwise_and(erode_hsv, erode_hsv, mask=mask)
            cv_show('res', inRange_hsv)  # 不必要，用于调试
        else:
            inRange_hsv1 = cv2.bitwise_and(erode_hsv, erode_hsv, mask=mask)
            cv_show('res1', inRange_hsv1)  # 不必要，用于调试
            inRange_hsv = cv2.add(inRange_hsv, inRange_hsv1)
            cv_show('res2', inRange_hsv)  # 不必要，用于调试
    return inRange_hsv


# 定义一个提取轮廓的函数
def extract_contour(img):
    inRange_gray = cv2.cvtColor(final_inRange_hsv, cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(inRange_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    return contours


# 定义一个寻找目标并绘制外接矩形的函数
def find_target(contours, draw_img):
    for c in contours:

        if cv2.contourArea(c) < 2000:  # 过滤掉较面积小的物体
            continue
        else:
            target_list.append(c)  # 将面积较大的物体视为目标并存入目标列表
    for i in target_list:  # 绘制目标外接矩形
        rect = cv2.minAreaRect(i)
        box = cv2.boxPoints(rect)
        cv2.drawContours(draw_img, [np.int0(box)], -1, (0, 255, 255), 2)
    return draw_img


# 定义一个绘制中心点坐标的函数
def draw_center(target_list, draw_img):
    for c in target_list:
        M = cv2.moments(c)  # 计算中心点的x、y坐标
        center_x = int(M['m10'] / M['m00'])
        center_y = int(M['m01'] / M['m00'])
        print('center_x:', center_x)  # 打印（返回）中心点的x、y坐标
        print('center_y:', center_y)

        cv2.circle(draw_img, (center_x, center_y), 7, 128, -1)  # 绘制中心点
        str1 = '(' + str(center_x) + ',' + str(center_y) + ')'  # 把坐标转化为字符串
        cv2.putText(draw_img, str1, (center_x - 50, center_y + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2,
                    cv2.LINE_AA)  # 绘制坐标点位

    return draw_img


###主函数部分
# 创建颜色字典
color_dist = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},
              'yellow': {'Lower': np.array([15, 160, 50]), 'Upper': np.array([35, 255, 255])},
              'green': {'Lower': np.array([50, 50, 50]), 'Upper': np.array([130, 255, 255])},
              'black':{'Lower':np.array([0, 0, 0]),'Upper':np.array([180, 255, 30])},
              'white':{'Lower':np.array([0, 0, 200]),'Upper':np.array([180, 30, 255])}
              }
# 目标颜色
target_color = ['red']
# 创建目标列表
target_list = []

img = cv2.imread(r'../yolov5-5.0/runs/detect/exp3/FmMRbndGh7.jpg', cv2.COLOR_BGR2RGB)  # 读入图像（直接读入灰度图）
draw_img = img.copy()  # 为保护原图像不被更改而copy了一份，下面对图像的修改都是对这个副本进行的
erode_hsv = good_thresh_img(img)
final_inRange_hsv = select_color_img(target_color, erode_hsv)
contours = extract_contour(final_inRange_hsv)
draw_img = find_target(contours, draw_img)
final_img = draw_center(target_list, draw_img)

cv_show('final_img', final_img)

