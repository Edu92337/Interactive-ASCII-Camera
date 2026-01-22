# Interactive-ASCII-Camera

An interactive Python application that converts webcam feed into ASCII art in real-time, with zoom control through hand gestures using computer vision.

## Description

This project captures video from your webcam and converts it into ASCII art in the terminal. The unique feature is interactive zoom control through hand gestures, detected using MediaPipe Hand Tracking. The wider you open your hand in front of the camera, the greater the zoom applied to the ASCII image.

## Features

- Real-time video to ASCII art conversion
- Interactive zoom control through hand gestures
- Detection of up to 2 hands simultaneously
- 25 levels of ASCII gradation (from light to dark)
- Smooth terminal interface with fluid updates

## Requirements

- Python 3.7+
- Working webcam
- MediaPipe Hand Landmarker model ([hand_landmarker.task](hand_landmarker.task))

## Dependencies

```bash
pip install opencv-python numpy pandas mediapipe
```

Or, if you prefer to create a virtual environment:

```bash
python -m venv vc
source vc/bin/activate  # On Windows: vc\Scripts\activate
pip install opencv-python numpy pandas mediapipe
```

## How to Use

1. Clone the repository:
```bash
git clone <https://github.com/Edu92337/Interactive-ASCII-Camera>
cd ASCII_VISION
```

2. Install dependencies:
```bash
pip install opencv-python numpy pandas mediapipe
```

3. Make sure the [hand_landmarker.task](hand_landmarker.task) file is in the project root directory

4. Run the program:
```bash
python main.py
```

5. Interact with the application:
   - Show your hand to the camera
   - Open or close your hand to control zoom
   - Press 'q' to exit

## How It Works

### ASCII Conversion

The program uses a scale of 25 ASCII characters ordered from lightest to darkest:

```
' ', '.', ',', ':', ';', '-', '=', '+', '*', '!', '?', '%', 'x', 'o', 'a', 'h', 'k', 'b', 'd', 'p', 'q', 'w', 'm', '#', '@'
```

Each pixel from the webcam frame is converted to grayscale and mapped to one of these characters based on its intensity.

### Gesture-Controlled Zoom

The system uses MediaPipe Hand Landmarker to:
1. Detect hand landmarks in real-time
2. Calculate the area occupied by the hand in the frame
3. Map this area to a zoom factor (1.0x to 3.0x)
4. Apply zoom by centering the region of interest

The wider your hand opening, the greater the zoom applied!

## Project Structure

```
ASCII_VISION/
├── main.py                    # Application entry point
├── webcam.py                  # Camera class with all the logic
├── hand_landmarker.task       # MediaPipe model for hand detection
├── README.md                  # This file

```
## Adjustable Parameters

In [webcam.py](webcam.py#L49-L50), you can adjust:

```python
char_ratio = 0.55   # Character aspect ratio
scale = 0.15        # ASCII art resolution scale
```

- `char_ratio`: Adjusts height/width proportion (characters are taller than wide)
- `scale`: Defines ASCII art resolution (lower values = more detail)

In [webcam.py](webcam.py#L105), you can adjust the zoom range:

```python
zoom = np.interp(hand_area, [0.02, 0.25], [1.0, 2.5])  # [min_area, max_area], [min_zoom, max_zoom]
```
