# USAGE
# python real_time_object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2

import face_detect
from dynamic_detact import dynamic_area_detect
from tracker import init_tracker
from car_num_location import car_brand_detect

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=False,
                default='MobileNetSSD_deploy.prototxt.txt',
                help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=False,
                default='MobileNetSSD_deploy.caffemodel',
                help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
                help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

# 需要方框标注的类
NEED_CLASSES = set(['car', 'person'])
# NEED_CLASSES = set(CLASSES)

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# 保存跟踪器对象
tracker_status = dict()
tracker_id = set(range(30))

ignore_area = []


def create_tracker(tracker_box, class_name):
    tracker = init_tracker(frame, tracker_box)
    tracker.id = tracker_id.pop()
    tracker.box = tracker_box
    tracker.CLASS = class_name
    tracker_status[tracker.id] = tracker


def target_detect(frame):
    """目标检测"""
    global net
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    # pass the blob through the network and obtain the detections and
    # predictions
    detections = net.forward()
    return detections


def handle_detections(detections, confidence=args["confidence"], x_offset=0, y_offset=0):
    global frame
    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the prediction
        conf = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        if conf > confidence:
            # extract the index of the class label from the
            # `detections`, then compute the (x, y)-coordinates of
            # the bounding box for the object
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            startX, startY, endX, endY = box.astype("int")

            class_name = CLASSES[idx]
            if class_name in NEED_CLASSES:
                # 继续检测人脸
                if class_name == 'person':
                    print('face location:', startY, endY, startX, endX)
                    face_detect.face_detect(frame[startY: endY, startX: endX])
                elif class_name == 'car':
                    brand_region = car_brand_detect(frame[startY: endY, startX, endX])

                    # 用绿线画出车牌轮廓
                    for box in brand_region:
                        x, y, w, h = box
                        cv2.rectangle(frame, (x + startX + x_offset, y + startY + y_offset),
                                      (x + startX + x_offset + w, y + startY + y_offset + h))

                # draw the prediction on the frame
                label = "{}: {:.2f}%".format(class_name,
                                             conf * 100)
                # 为每个目标创建跟踪器
                tracker_box = (startX+x_offset, startY+y_offset, endX+x_offset-startX, endY+y_offset - startY)
                ignore_area.append(tracker_box)
                create_tracker(tracker_box, class_name)

                cv2.rectangle(frame, (startX + x_offset, startY + y_offset), (endX + x_offset, endY + y_offset),
                              COLORS[idx], 2)
                # 标注文字
                y = startY+y_offset - 15 if startY+y_offset - 15 > 15 else startY+y_offset + 15
                cv2.putText(frame, label, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

    # show the output frame
    cv2.imshow("Frame", frame)

    # update the FPS counter
    fps.update()


############## start ##################

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
print("[INFO] starting video stream...")
video_file = 'test_video.flv'
vs = VideoStream(video_file).start()
# vs = VideoStream(src=1).start()
time.sleep(2.0)
fps = FPS().start()

# loop over the frames from the video stream
start_time = time.time()

frame = vs.read()
if frame is None:
    exit('Video Input Error! 输入错误！')
# grab the frame from the threaded video stream and resize it
# to have a maximum width of 800 pixels
frame = imutils.resize(frame, width=800)
# grab the frame dimensions and convert it to a blob
h, w = frame.shape[:2]

detections = target_detect(frame)
handle_detections(detections)

# 后续帧
while True:
    frame = vs.read()
    if frame is None:
        exit('Video Input Error! 输入错误！')
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 800 pixels
    frame = imutils.resize(frame, width=800)
    for tracker in tracker_status.values():
        # Update tracker
        ok, bbox = tracker.update(frame)
        # print(ok, bbox)

        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        else:
            # Tracking failure
            # 更新跟踪器状态
            tracker_status.pop(tracker.id)
            tracker_id.add(tracker.id)
            ignore_area.remove(tracker.box)

    dynamic_area = dynamic_area_detect(frame, ignore_area)
    for area in dynamic_area:
        x, y, w, h = area
        detections = target_detect(frame[y: y + h, x:x + w])
        handle_detections(detections, x_offset=x, y_offset=y)

    # if the `q` key was pressed, break from the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    cv2.imshow("Frame", frame)
    fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
