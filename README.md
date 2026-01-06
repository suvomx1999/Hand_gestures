# Virtual AI Mouse 🖱️

Control your computer mouse using hand gestures with your webcam!

## �️ Installation & Setup

1.  **Prerequisites**
    *   Make sure you have **Python 3.7+** installed.

2.  **Install Dependencies**
    Open your terminal/command prompt in the project folder and run:
    ```bash
    pip install -r requirements.txt
    ```

## �🚀 How to Run

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
