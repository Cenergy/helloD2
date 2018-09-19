from django.test import TestCase

# Create your tests here.
#coding=utf8
import cv2
import numpy as np
from tqdm import tqdm
import pytesseract
import xlwt
import time

time_start = time.time()



CV2_WAIT_TIME = 1
cv2.namedWindow('img', cv2.WINDOW_NORMAL)
#读取文件
img_gray = cv2.imread('4.jpg', cv2.IMREAD_GRAYSCALE)


img_thresh = cv2.adaptiveThreshold(255 - img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                                         cv2.THRESH_BINARY, 15, -8)

# cv2.imshow('img', img_thresh)
# cv2.waitKey(0)

cv2.imshow('img', img_thresh)
cv2.waitKey(CV2_WAIT_TIME)

img_horizontal = img_thresh.copy()
img_vertical = img_thresh.copy()

n_scale = 20
n_hori_size = int(img_horizontal.shape[1] / n_scale)
horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (n_hori_size, 1))

#先腐蚀再膨胀
img_horizontal = cv2.erode(img_horizontal, horizontalStructure, (-1, -1))
horizontal = cv2.dilate(img_horizontal, horizontalStructure, (-1, -1))
# #将图像左移，删补
# horizontal = np.delete(horizontal, 1, axis=1)
# horizontal = np.insert(horizontal, -1, values=0, axis=1)
# cv2.imshow("img", horizontal)
# cv2.waitKey(CV2_WAIT_TIME)


M = np.float32([[1,0,-1],[0,1,0]]) #图像往下移动一个像素
# cv2.getAffineTransform()
horizontal = cv2.warpAffine(horizontal, M, horizontal.shape[::-1])
# print(horizontal.shape)
cv2.imshow("img", horizontal)
cv2.waitKey(CV2_WAIT_TIME)

n_vert_size = int(img_horizontal.shape[0] / n_scale)
verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, n_vert_size))
img_vertical = cv2.erode(img_vertical, verticalStructure, (-1, -1))
vertical = cv2.dilate(img_vertical, verticalStructure, (-1, -1))
cv2.imshow("img", vertical)
cv2.waitKey(CV2_WAIT_TIME)

cv2.imshow("img", horizontal+ vertical)
cv2.waitKey(CV2_WAIT_TIME)

img_dot = cv2.bitwise_and(horizontal, vertical)
cv2.imshow('img', img_dot)
cv2.waitKey(CV2_WAIT_TIME)

# M = np.float32([[1,0,0],[0,1,5]]) #图像往下移动5个像素
# # cv2.getAffineTransform()
# dst = cv2.warpAffine(horizontal, M, horizontal.shape[::-1])
# cv2.imshow("img", vertical - dst)
# cv2.waitKey(CV2_WAIT_TIME)

def isolate(img):
    idx=np.argwhere(img==255)
    rows,cols=img.shape

    for i in range(idx.shape[0]):
        c_row=idx[i,0]
        c_col=idx[i,1]
        if c_col+1<cols and c_row+1<rows:
            img[c_row,c_col+1]=1
            img[c_row+1,c_col]=1
            img[c_row+1,c_col+1]=1
        if c_col+2<cols and c_row+2<rows:
            img[c_row+1,c_col+2]=1
            img[c_row+2,c_col]=1
            img[c_row,c_col+2]=1
            img[c_row+2,c_col+1]=1
            img[c_row+2,c_col+2]=1
    return img

img_dot = isolate(img_dot)
cv2.imshow('img', img_dot)
# cv2.imwrite('dot.jpg', img_dot)
cv2.waitKey(CV2_WAIT_TIME)



#根据点图切割表格
pos_dot = np.where(img_dot==255)
pos_points = zip(pos_dot[1], pos_dot[0]) #(x,y)
# list_pos_points = [pos for pos in pos_points]
# print('\nlist_pos_points:\n',list_pos_points)
# print('\n')


table_pos = list()
pos_temp = None
list_row = []
for point in pos_points:
    if pos_temp is None:
        pos_temp = point
    if pos_temp[0] - point[0] <= 0 :
        #在同一行
        list_row.append(point)
        pos_temp = point
    elif abs(pos_temp[0] - point[0]) < 9:
        #去掉干扰
        continue
    else:
        table_pos.append(list_row)
        list_row = []
        list_row.append(point)
        pos_temp = None
table_pos.append(list_row)
print(table_pos)

#对表格进行一次整理
#存在【【（608，464）,（1206, 464）】,【(908, 465)】】的情况
#整合为【【（608，464）, (908, 465)】,（1206, 464）】】】

bool_next_used = False
n_used = 0
table_pos_copy = table_pos[:]
for n_row, row_pos in enumerate(table_pos_copy):
    if n_row+1 == len(table_pos_copy):
        break
    if bool_next_used:
        bool_next_used = False
        n_used -= 1
        continue
    tmp = table_pos_copy[n_row+1]
    if table_pos_copy[n_row+1][0][1] - row_pos[0][1] < 3:
        # print(table_pos[n_row+1][0][1], row_pos[0][1])
        table_pos[n_row + n_used] += table_pos[n_row+1 + n_used]
        table_pos[n_row + n_used].sort(key=lambda x: x[0])
        # print(len(table_pos))
        # print(row_pos, '----', table_pos_copy[n_row + 1], '\n')
        del(table_pos[n_row+1+n_used])
        # print(len(table_pos))
        bool_next_used = True


def check_have_no_vertical_line(t_point, img):

    w, h = t_point
    h += 10
    if t_point == (1057, 136):
        print('***')
        print(img[h, w] != 255)
        print('***')
        print(img[136, 1057])
    return img[h, w] != 255


list_roi = list()
# last_pos = None
for n_row, row_pos in enumerate(table_pos):
    if n_row+1 == len(table_pos):
        break
    for n_col, pos in enumerate(row_pos):
        if n_col+1 == len(row_pos):
            break
        # roi = [*pos, *table_pos[n_row+1][n_col+1], n_row, n_col]


        if len(row_pos) != len(table_pos[n_row+1]):
            # try:
            roi = [*pos, row_pos[n_col+1][0], table_pos[n_row+1][0][1], n_row, n_col, 'dif']
            # except:
                # print(pos)
        else:
            # try:
            roi = [*pos, *table_pos[n_row+1][n_col+1], n_row, n_col, 'same']
            # except(IndexError):
            #     #存在上下行元素个数不统一的情况，直接忽略
            #     break

        if check_have_no_vertical_line(pos, vertical) and n_col>0:
            #判断是否有竖线
            print(list_roi[-1])
            print(pos)
            # print(list_roi[-1][:2])
            list_roi[-1][2:4] = roi[2:4]
            # print(list_roi)
        else:

        # print(roi)
            list_roi.append(roi)
        # list_roi.append(roi)
# print(list_roi)



img_dot_color = cv2.merge([img_dot]*3)

#将切块的表格分别识别
print('\n\n\n\n')
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
# result = pytesseract.image_to_boxes(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), lang='chi_sim_fast')
book = xlwt.Workbook()
sheet = book.add_sheet('sheet1')
for pos in tqdm(list_roi):
    x1, y1, x2, y2, n_row, n_col, _ = pos
    if (x2-x1<10 or y2-y1<10):
        continue
    img_dot_color = cv2.rectangle(img_dot_color, (x1, y1), (x2, y2), color=(255, 255, 255), thickness=7)
    img_recogntion = img_gray[y1+4:y2-2, x1+4:x2-2]
    # img_recogntion = img_thresh[y1+4:y2-2, x1+4:x2-2]
    cv2.imshow('img', img_dot_color)
    # cv2.imshow('img', img_recogntion)
    cv2.waitKey(CV2_WAIT_TIME)
    if np.sum(img_recogntion/255./img_recogntion.size) > 0.99:
        #空白
        continue
    result = pytesseract.image_to_string(img_recogntion, lang='chi_sim', config='--psm 7')
    # print(result)

    sheet.write(n_row, n_col, result)

book.save("1.xls")

cv2.waitKey(0)

print("cost time:", -time_start + time.time())