import cv2
import time
import numpy as np

i = 0
j = 1
timeF = 120  #多少帧截取一次

camera = cv2.VideoCapture(0) # 参数0表示第一个摄像头
bs = cv2.createBackgroundSubtractorKNN(history=500, dist2Threshold=400.0, detectShadows=False)
es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

while True:
    i = i + 1
    grabbed, frame = camera.read()
    gb = cv2.GaussianBlur(frame, ksize=(9, 9), sigmaX=0, sigmaY=0)  #高斯模糊
    fgmask = bs.apply(gb) # 背景分割器，该函数计算了前景掩码

    # 二值化阈值处理，前景掩码含有前景的白色值以及阴影的灰色值，在阈值化图像中，将非纯白色（244~255）的所有像素都设为0，而不是255
    th = cv2.threshold(fgmask.copy(), 244, 255, cv2.THRESH_BINARY)[1]

    # 下面就跟基本运动检测中方法相同，识别目标，检测轮廓，在原始帧上绘制检测结果
    dilated = cv2.dilate(th, es, iterations=2)  # 形态学膨胀
    # 该函数计算一幅图像中目标的轮廓
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #实时的时间显示
    cv2.putText(frame, "Now Time: {}".format(str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))),
                (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    for c in contours:
        # 对轮廓设置最小区域，对检测结果降噪
        if cv2.contourArea(c) > 2000:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

            if  (i % timeF == 0):
                address = './Image/' + str(j) + '.jpg'
                cv2.imwrite(address, frame)
                print('save image:', j)
                j = j+1

    cv2.imshow('Grey', th)
    cv2.imshow('Original', frame)

    key = cv2.waitKey(1) & 0xFF

    # 按'q'健退出循环
    if key == ord('q'):
        break

#一切就绪后，释放捕获
camera.release()
cv2.destroyAllWindows()
