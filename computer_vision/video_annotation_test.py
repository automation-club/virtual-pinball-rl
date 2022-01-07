import numpy as np
import cv2

cap = cv2.VideoCapture("../datasets/playing-phone-trim-horizontal.mp4")

current_state = False
annotation_list = []

while(True):
    # Read one frame.
    ret, frame = cap.read()
    if not ret:
        break

    # Show one frame.
    cv2.imshow('frame', frame)

    # Check, if the space bar is pressed to switch the mode.
    if cv2.waitKey(1) & 0xFF == ord(' '):
        current_state = not current_state

    annotation_list.append(current_state)

# Convert the list of boolean values to a list of int values.
annotation_list = map(int, annotation_list)
print (annotation_list)

cap.release()
cv2.destroyAllWindows()