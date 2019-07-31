import cv2
import sys

trackerTypes = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
bboxes = []


def _create_tracker_by_name(tracker_type):
    # Create a tracker based on tracker name
    if tracker_type == trackerTypes[0]:
        tracker = cv2.TrackerBoosting_create()
    elif tracker_type == trackerTypes[1]:
        tracker = cv2.TrackerMIL_create()
    elif tracker_type == trackerTypes[2]:
        tracker = cv2.TrackerKCF_create()
    elif tracker_type == trackerTypes[3]:
        tracker = cv2.TrackerTLD_create()
    elif tracker_type == trackerTypes[4]:
        tracker = cv2.TrackerMedianFlow_create()
    elif tracker_type == trackerTypes[5]:
        tracker = cv2.TrackerGOTURN_create()
    elif tracker_type == trackerTypes[6]:
        tracker = cv2.TrackerMOSSE_create()
    elif tracker_type == trackerTypes[7]:
        tracker = cv2.TrackerCSRT_create()
    else:
        tracker = None
        print('Incorrect tracker name')
        print('Available trackers are:')
        for t in trackerTypes:
            print(t)
    return tracker


def init_multi_tracker(frame, bboxes, tracker_type='KCF'):
    # Create MultiTracker object
    multiTracker = cv2.MultiTracker_create()

    # 使用第一帧和边界框初始化单个对象跟踪器，
    # 该边界框指示我们想要跟踪的对象的位置
    # MultiTracker将此信息传递给它内部包装的单个目标跟踪器。
    for bbox in bboxes:
        multiTracker.add(_create_tracker_by_name(tracker_type), frame, bbox)

    return multiTracker


def init_tracker(frame, box, tracker_type='KCF'):
    """box: [x, y, w, h]"""
    tracker = _create_tracker_by_name(tracker_type)
    tracker.init(frame, box)
    return tracker


if __name__ == '__main__':

    # Read video
    # video = cv2.VideoCapture("chaplin.mp4")
    # camera
    video = cv2.VideoCapture(0)

    # Exit if video not opened.
    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()

    # 单目标检测
    # 格式：左上角 x, y, w, h
    # bbox = (287, 23, 86, 320)
    bbox = (231, 197, 160, 200)

    # Initialize tracker with first frame and bounding box
    tracker = init_tracker(frame, bbox)

    # 多目标检测器
    # bboxex = [(287, 23, 86, 320)]
    # tracker = init_multi_tracker(frame, bboxes, 'KCF')

    while True:
        ok, frame = video.read()
        if not ok:
            break

        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        ok, bbox = tracker.update(frame)
        # print(ok, bbox)

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        else:
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        # Display tracker type on frame
        # cv2.putText(frame, tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

        # Display result
        cv2.imshow("Tracking", frame)

        # Exit if ESC pressed
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
