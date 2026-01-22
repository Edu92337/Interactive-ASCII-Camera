import cv2
import numpy as np
import pandas as pd
import webcam

if __name__ == "__main__":
    cam = webcam.Camera()
    cam.get_pixels_intensity()
    