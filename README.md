# Virtual AI Mouse 🖱️

## 📖 Project Description
The **Virtual AI Mouse** is a computer vision-based application that allows you to control your computer's mouse cursor and perform system actions using simple hand gestures. By leveraging a standard webcam, it eliminates the need for physical hardware like a mouse or trackpad.

Built with **Python**, **OpenCV**, and **MediaPipe**, this project detects hand landmarks in real-time and maps them to screen coordinates. It supports a variety of intuitive gestures for navigation, clicking, scrolling, and even volume control, making it a futuristic and touch-free way to interact with your PC.

### ✨ Key Features
*   **Touch-Free Navigation**: Move the cursor just by pointing your finger.
*   **Gesture Clicking**: Perform Left and Right clicks with pinch gestures.
*   **Smart Smoothing**: Adaptive algorithm to reduce cursor jitter and lag.
*   **System Control**: Adjust volume and scroll through pages using natural hand motions.
*   **Real-Time Performance**: Optimized for low latency on standard CPUs.

## 🛠️ Installation & Setup

1.  **Prerequisites**
    *   Make sure you have **Python 3.7+** installed.

2.  **Install Dependencies**
    Open your terminal/command prompt in the project folder and run:
    ```bash
    pip install -r requirements.txt
    ```

## �� How to Run

1.  **Start the Application**
    Run the following command in your terminal:
    ```bash
    python3 virtual_mouse.py
    ```

2.  **Usage**
    *   The webcam window will open.
    *   Show your hand to the camera (keep it about 1-2 feet away).
    *   Use the gestures below to control your mouse.

## ✋ Gesture Commands

| Action | Hand Gesture | Details |
| :--- | :--- | :--- |
| **Move Cursor** | ☝️ **Index Finger Up** | Keep Thumb, Middle, Ring, Pinky down. |
| **Left Click** | ✌️ **Index + Middle Up** | Pinch fingers together (< 40px distance). |
| **Right Click** | 🤘 **Middle + Ring Up** | Pinch fingers together (< 40px distance). |
| **Volume Control** | 👆 **Thumb + Index Up** | **Apart** = Volume Up 🔊<br>**Close** = Volume Down 🔇 |
| **Scroll Mode** | 🖐️ **Open Hand (All 5 Up)** | **Hand Top** = Scroll Up ⬆️<br>**Hand Bottom** = Scroll Down ⬇️ |

## ⚙️ Configuration
You can adjust settings in `virtual_mouse.py`:
*   `frameR`: Frame reduction (padding).
*   `smoothening`: Mouse movement smoothness.

## 🛑 Exit
Press **'q'** on your keyboard to close the application.
