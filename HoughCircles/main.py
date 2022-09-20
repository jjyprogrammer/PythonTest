import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("D:/pyTest/HoughCircles/1.png")
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #灰度图像

plt.subplot(121),plt.imshow(gray,'gray')
plt.xticks([]),plt.yticks([])
#使用HoughCircles对灰度图像进行霍夫变换
circles1 = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,
100,param1=100,param2=30,minRadius=50,maxRadius=100)
circles = circles1[0,:,:] #提取为二维
circles = np.uint16(np.around(circles)) #四舍五入，取整
for i in circles[:]:
    cv2.circle(img,(i[0],i[1]),i[2],(255,0,0),5) #画圆
    cv2.circle(img,(i[0],i[1]),2,(255,0,255),10) #画圆心

plt.subplot(122),plt.imshow(img)
plt.xticks([]),plt.yticks([]);