# Air-Draw — Gesture-Controlled Drawing App

A touchless drawing application that lets you sketch in the air using just your hand — no mouse, stylus, or touchscreen required. Built with OpenCV and MediaPipe's Hand Landmarker model.

## Features
- Real-time hand tracking via webcam
- Pinch-to-draw gesture: bring thumb and index finger together to start drawing, release to lift the "pen"
- Live canvas overlay rendered directly on the video feed
- Smooth, responsive tracking using MediaPipe's Tasks API

## Tech Stack
- Python 3
- OpenCV (video capture, canvas rendering)
- MediaPipe Tasks API (`hand_landmarker.task` model) for hand landmark detection

## How It Works
1. The webcam feed is captured frame-by-frame using OpenCV.
2. Each frame is passed to MediaPipe's Hand Landmarker, which returns 21 hand landmark coordinates.
3. The distance between the thumb tip and index fingertip is measured — when it drops below a threshold, it's interpreted as a "pinch," triggering draw mode.
4. While pinched, the fingertip position is tracked frame-to-frame and used to draw continuous lines onto a transparent canvas layer.
5. The canvas is overlaid on top of the live video feed in real time.

## Setup
```bash
pip install opencv-python mediapipe

# Download the hand landmarker model
# (from MediaPipe's model repository)

python3 air_draw.py
```

## Challenges Solved
- Translating raw hand landmark coordinates into a reliable pinch gesture
- Maintaining a persistent canvas overlay without flickering across frames
- Tuning pinch-distance thresholds for natural, responsive drawing

## License
MIT
