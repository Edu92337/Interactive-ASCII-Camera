import cv2
import numpy as np
from mediapipe import tasks
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import mediapipe as mp
import os
import time

# ASCII characters from light to dark
chars = np.array([
    ' ', '.', ',', ':', ';', '-', '=', '+', '*', '!',
    '?', '%', 'x', 'o', 'a', 'h', 'k', 'b', 'd', 'p',
    'q', 'w', 'm', '#', '@'
])

lut = chars[(np.arange(256) * (len(chars) - 1)) // 255]


class Camera:
    def __init__(self):
        """Initialize the Camera class and hand landmarker."""
        # Initialize hand landmarker
        base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=2,
            min_hand_detection_confidence=0.3,
            min_hand_presence_confidence=0.3,
            min_tracking_confidence=0.3)
        self.detector = vision.HandLandmarker.create_from_options(options)
        self.frame_timestamp = 0
    
    def init_webcam(self): 
        """Initialize webcam feed."""
        cam = cv2.VideoCapture(0) 
        online = True 
        while online: 
            status,frame = cam.read() 
            if not status or cv2.waitKey(1)&0xff == ord('q'): 
                online = False 
            cv2.imshow("webcam",frame)
            
    def get_pixels_intensity(self):
        """Capture webcam feed and convert to ASCII art with zoom controlled by hand gestures."""
        cam = cv2.VideoCapture(0)

        char_ratio = 0.55
        scale = 0.15
        while True:
            status, frame = cam.read()
            if not status:
                break
            cv2.imshow("webcam", frame)

            # ASCII
            zoomed_frame = self.zoom_frame(frame)
            if isinstance(zoomed_frame, float):
                zoomed_frame = frame
            
            gray = cv2.cvtColor(zoomed_frame, cv2.COLOR_BGR2GRAY)
            h, w = gray.shape
            new_w = int(w * scale)
            new_h = int(h * scale * char_ratio)

            gray = cv2.resize(
                gray, (new_w, new_h), interpolation=cv2.INTER_AREA
            )
            
            ascii_frame = lut[gray]
            ascii_image = "\n".join("".join(row) for row in ascii_frame)

            os.system("clear")
            print(ascii_image)

            if cv2.waitKey(1) & 0xff == ord('q'):
                break

            time.sleep(0.03)

        cam.release()
        cv2.destroyAllWindows()

    def zoom_frame(self, frame):
        """Zoom the frame based on hand landmarks detected."""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        self.frame_timestamp = int(time.time() * 1000)
        result = self.detector.detect_for_video(mp_image, self.frame_timestamp)

        h, w, _ = frame.shape

        if not result.hand_landmarks:
            return frame  # SEMPRE retorna imagem

        landmarks = result.hand_landmarks[0]
        xs = [lm.x for lm in landmarks]
        ys = [lm.y for lm in landmarks]

        hand_area = (max(xs) - min(xs)) * (max(ys) - min(ys))

        # mão controla ZOOM (campo de visão)
        zoom = np.interp(hand_area, [0.02, 0.25], [1.0, 2.5])
        zoom = float(np.clip(zoom, 1.0, 3.0))

        crop_w = int(w / zoom)
        crop_h = int(h / zoom)

        cx, cy = w // 2, h // 2

        x1 = max(cx - crop_w // 2, 0)
        y1 = max(cy - crop_h // 2, 0)
        x2 = min(cx + crop_w // 2, w)
        y2 = min(cy + crop_h // 2, h)

        cropped = frame[y1:y2, x1:x2]

        # volta para o tamanho original
        zoomed = cv2.resize(cropped, (w, h), interpolation=cv2.INTER_LINEAR)

        return zoomed


