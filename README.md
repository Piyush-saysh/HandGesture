# **Hand Gesture Control for Computer Actions**

## **Overview**

**This Python project** leverages hand gesture recognition to control various computer actions such as cursor movement, screen recording, screenshots, adjusting brightness, and controlling the volume. It uses **OpenCV** for webcam capture, **HandTrackingModule** for hand gesture detection, and **pyautogui** for interacting with the operating system. The system detects specific finger movements and gestures to trigger actions like clicking, scrolling, or system functions.

## **Features**

- **Cursor Control**: Move the cursor using hand gestures, with smoothing for more natural movements.
- **Clicking and Scrolling**: Perform left-click, right-click, and scroll actions using finger gestures.
- **Screen Recording**: Start and stop screen recording with a specific hand gesture.
- **Screenshots**: Take screenshots and save them with timestamps on the desktop.
- **Brightness Control**: Increase or decrease screen brightness using hand gestures.
- **Volume Control**: Adjust the system's volume based on hand distance.

## **Setup**

1. **Dependencies**: 
   - Install the required libraries:
   ```bash
   pip install opencv-python pyautogui numpy osascript
