import os
import cv2

# 加载人脸特征库
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# 人脸计数
face_num = len(os.listdir(os.path.join('data', 'face')))


def face_detect(img):
    """检测并保存人脸"""
    global face_num
    if img is None:
        return
    rects = face_cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)
    for (x, y, w, h) in rects:
        # 保存人脸
        cv2.imwrite(os.path.join('data', 'face', str(face_num) + '.jpg'), img[y:y+h, x:x+w, :])
        face_num += 1
        print('save face', face_num)
        # 用矩形圈出人脸
        # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv2.imshow('face', img)


def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
