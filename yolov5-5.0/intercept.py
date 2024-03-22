import os
import cv2
from LPRNet_Pytorch.detect1 import detectImage

def intercept1(image_path):
    full_path = os.path.join("..\\yolov5-5.0", image_path)
    # img_path = '../yolov5-5.0/runs/detect/exp14/'  # 图片路径
    # label_path = '../yolov5-5.0/runs/detect/exp14/labels/'  # txt文件路径
    # save_path = '../yolov5-5.0/runs/detect/exp14/'  # 保存路径

    # 指定路径和文件夹名称
    folder_path = full_path
    folder_name = "plates"

    # 使用 os.path.join() 将路径和文件夹名称连接起来
    folder_path = os.path.join(folder_path, folder_name)

    # 使用 os.makedirs() 创建文件夹
    os.makedirs(folder_path)

    img_path = full_path + "\\pic\\"  # 图片路径
    label_path = full_path + "\\labels\\"  # txt文件路径
    save_path = full_path + "\\plates\\"  # 保存路径

    img_total = []
    label_total = []
    imgfile = os.listdir(img_path)
    labelfile = os.listdir(label_path)
    outputfile = []

    for filename in imgfile:
        name, type = os.path.splitext(filename)
        if type == '.png' or type == '.jpg':
            img_total.append(name)

    for filename in labelfile:
        name, type = os.path.splitext(filename)
        if type == '.txt':
            label_total.append(name)

    for _img in img_total:
        if _img in label_total:
            filename_img = _img + '.jpg'
            path = os.path.join(img_path, filename_img)
            # print(path)
            img = cv2.imread(path)  # 读取图片，结果为三维数组
            filename_label = _img + '.txt'
            w = img.shape[1]  # 图片宽度(像素)
            h = img.shape[0]  # 图片高度(像素)
            n = 1
            # 打开文件，编码格式'utf-8','r+'读写
            with open(os.path.join(label_path, filename_label), "r+", encoding='utf-8', errors="ignor") as f:
                for line in f:
                    msg = line.split(" ")  # 根据空格切割字符串，最后得到的是一个list
                    x1 = int((float(msg[1]) - float(msg[3]) / 2) * w)  # x_center - width/2
                    y1 = int((float(msg[2]) - float(msg[4]) / 2) * h)  # y_center - height/2
                    x2 = int((float(msg[1]) + float(msg[3]) / 2) * w)  # x_center + width/2
                    y2 = int((float(msg[2]) + float(msg[4]) / 2) * h)  # y_center + height/2
                    filename_last = _img + "_" + str(n) + ".jpg"
                    outputfile.append(filename_last)
                    # print(filename_last)
                    img_roi = img[y1:y2, x1:x2]  # 剪裁，roi:region of interest
                    cv2.imwrite(os.path.join(save_path, filename_last), img_roi)
                    # print(os.path.join(save_path, filename_last))
                    n = n + 1
        else:
            continue

    for filenamei in outputfile:
        interceptFilename = str(image_path) + "\\plates\\" + filenamei
        detectImage(interceptFilename)


