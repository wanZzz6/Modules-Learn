import cv2

# create Background Subtractor objects
bs = cv2.createBackgroundSubtractorKNN(detectShadows=True)

_es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 4))


def dynamic_area_detect(frame, ignore_area=[]):
    """ignore_area： 忽略检测区域[[x, y, w, h]"""
    global bs
    fgmask = bs.apply(frame)

    fg2 = fgmask.copy()
    # 二值化阈值处理
    th = cv2.threshold(fg2, 244, 255, cv2.THRESH_BINARY)[1]
    for i in ignore_area:
        pass

    # 形态学膨胀
    dilated = cv2.dilate(th, _es, iterations=2)
    contours, hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    result = []
    for c in contours:
        if cv2.contourArea(c) > 500:
            # 该函数计算矩形的边界框
            (x, y, w, h) = cv2.boundingRect(c)
            result.append((x, y, w, h))

    cv2.imshow("mog", fgmask)
    cv2.imshow("thresh", th)
    return result


if __name__ == '__main__':

    camera = cv2.VideoCapture(0)  # 参数0表示第一个摄像头
    # 判断视频是否打开
    if camera.isOpened():
        print('Open')
    else:
        print('摄像头未打开')

    # 测试用,查看视频size
    # size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
    #         int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # print('size:' + repr(size))

    while True:
        ret, frame = camera.read()
        areas = dynamic_area_detect(frame)

        for c in areas:
            (x, y, w, h) = c
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

        cv2.imshow("detection", frame)
        if cv2.waitKey(24) & 0xff == 27:
            break
    camera.release()
    cv2.destroyAllWindows()
