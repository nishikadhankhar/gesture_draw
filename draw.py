import cv2
import mediapipe as mp
import numpy as np
import math
import time

from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

model_path = "/Users/nishi/gesture_draw/hand_landmarker.task"

base_options = mp_python.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    running_mode=vision.RunningMode.VIDEO
)
landmarker = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
h, w, _ = frame.shape
canvas = np.zeros((h, w, 3), dtype=np.uint8)

prev_x, prev_y = None, None
drawing = False
pinch_threshold = 40
start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    timestamp_ms = int((time.time() - start_time) * 1000)

    result = landmarker.detect_for_video(mp_image, timestamp_ms)

    if result.hand_landmarks:
        lm = result.hand_landmarks[0]
        index_tip = lm[8]
        thumb_tip = lm[4]

        ix, iy = int(index_tip.x * w), int(index_tip.y * h)
        tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)

        dist = math.hypot(ix - tx, iy - ty)
        drawing = dist < pinch_threshold

        if drawing:
            if prev_x is not None:
                cv2.line(canvas, (prev_x, prev_y), (ix, iy), (0, 0, 255), 5)
            prev_x, prev_y = ix, iy
        else:
            prev_x, prev_y = None, None

        cv2.circle(frame, (ix, iy), 8, (0, 255, 0), -1)
    else:
        prev_x, prev_y = None, None

    combined = cv2.addWeighted(frame, 0.6, canvas, 0.8, 0)
    cv2.imshow("Air Draw", combined)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        canvas = np.zeros((h, w, 3), dtype=np.uint8)

cap.release()
cv2.destroyAllWindows()
