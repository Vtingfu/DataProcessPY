import subprocess as sp
import cv2
import sys
import queue
import threading

frame_queue = queue.Queue()
rtmpUrl = "rtmp://IP地址/live/test"
camera_path = 'rtmp://172.27.132.103:1935/live/home'

# 获取摄像头参数
cap = cv2.VideoCapture(camera_path)
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# print(fps, width, height)

# ffmpeg command
command = ['ffmpeg',
           '-y',
           'rawvideo',
           '-vcodec', 'rawvideo',
           '-pix_fmt', 'bgr24',
           '-s', "{}x{}".format(width, height),
           '-r', str(fps),
           '-c:v', 'libx264',
           '-pix_fmt', 'yuv420p',
           '-preset', 'ultrafast',
           '-f', 'flv',
           '-g', '5',
           rtmpUrl]


# 读流函数
def Video():
        vid = cv2.VideoCapture(camera_path)
    if not vid.isOpened():
        raise IOError("could't open webcamera or video")
    while (vid.isOpened()):
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    Video()