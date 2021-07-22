import cv2
import numpy as np


# 定义保存图片函数
# image:要保存的图片名字
# addr；图片地址与相片名字的前部分
# num: 相片，名字的后缀。int 类型

camera = cv2.VideoCapture(0) # 参数0表示第一个摄像头

# 读取视频文件
#videoCapture = cv2.VideoCapture("test.mp4")
# 通过摄像头的方式
# videoCapture=cv2.VideoCapture(1)

# 读帧
success, frame = camera.read()

i = 0
timeF = 1000  #多少帧截取一次
j = 0

while success:
    i = i + 1

    if (i % timeF == 0):
        j = j + 1
        address = './Image/' + str(j) + '.jpg'
        cv2.imwrite(address, frame)
        print('save image:', i)

        if cv2.waitKey(1) & 0xFF == ord('q'):   #q退出
            break

    cv2.imshow('Original', frame)

#一切就绪后，释放捕获
camera.release()
cv2.destroyAllWindows()