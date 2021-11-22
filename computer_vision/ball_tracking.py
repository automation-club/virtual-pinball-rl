import cv2

VIDEO_PATH = "../datasets/playing-phone-trim-horizontal.mp4"

tracker = cv2.TrackerKCF_create()

vs = cv2.VideoCapture(VIDEO_PATH)

ok, frame = vs.read()
bounding_box = cv2.selectROI("Select Bounding Box", frame, fromCenter=True, showCrosshair=True)
success = tracker.init(frame, bounding_box)

while True:
    ok, frame = vs.read()
    success, bbox = tracker.update(frame)
    if success:
        x, y, h, w = [int(pos) for pos in bbox]
        cv2.rectangle()

# while True:
#     ok, frame = vs.read()
#
#     if bounding_box is not None:
#
#         ok, box = tracker.update(frame)
#
#         if ok:
#             x, y, w, h = [int(pos) for pos in box]
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255,0), thickness=5)
#
#     cv2.imshow("frame", frame)
#     key = cv2.waitKey(1)
#
#     if key == ord('s'):
#         bounding_box = cv2.selectROI("frame", frame, fromCenter=False, showCrosshair=True)
#         tracker