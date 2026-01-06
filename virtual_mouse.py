import cv2
import numpy as np
import hand_detector as hd
import time
import pyautogui
import os

# --- Configuration ---
wCam, hCam = 640, 480
frameR = 100  # Frame Reduction (padding from edges)
smoothening = 7  # Higher value = smoother but more lag
# ---------------------

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
# cap.set(3, wCam)
# cap.set(4, hCam)

detector = hd.HandDetector(maxHands=1)
wScr, hScr = pyautogui.size()

print("Virtual Mouse Started...")

while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    if not success:
        print("Error: Failed to capture image from camera.")
        break
        
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # Index finger tip
        x2, y2 = lmList[12][1:] # Middle finger tip
        x3, y3 = lmList[16][1:] # Ring finger tip
        x4, y4 = lmList[4][1:]  # Thumb tip

        # 3. Check which fingers are up
        
        fingers = []
        # Thumb (4)
        # Robust Check: Distance between Thumb Tip (4) and Index MCP (5)
        # If distance is large -> Thumb is Open. If small -> Thumb is Closed.
        thumb_index_dist = ((lmList[4][1] - lmList[5][1])**2 + (lmList[4][2] - lmList[5][2])**2)**0.5
        
        # Threshold can be adjusted (e.g., 50-60 pixels)
        if thumb_index_dist > 60:
            fingers.append(1) # Thumb Open
        else:
            fingers.append(0) # Thumb Closed

        # Index (8)
        if lmList[8][2] < lmList[6][2]:
            fingers.append(1)
        else:
            fingers.append(0)
            
        # Middle (12)
        if lmList[12][2] < lmList[10][2]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Ring (16)
        if lmList[16][2] < lmList[14][2]:
            fingers.append(1)
        else:
            fingers.append(0)
            
        # Pinky (20)
        if lmList[20][2] < lmList[18][2]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers Index: [Thumb, Index, Middle, Ring, Pinky]

        # 4. Only Index Finger : Moving Mode
        # Ensure Thumb is DOWN (fingers[0] == 0) to avoid conflict with Volume
        if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[0] == 0:
            # 5. Convert Coordinates
            
            x_mapped = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y_mapped = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            # 6. Smoothen Values (Adaptive)
            # Calculate distance moved
            move_dist = ((x_mapped - plocX) ** 2 + (y_mapped - plocY) ** 2) ** 0.5
            
            # Jitter Threshold: Ignore very small movements to keep mouse stable
            if move_dist < 3:
                x_mapped, y_mapped = plocX, plocY
            elif move_dist > 100:
                smoothening = 2 # Fast movement -> less smoothing
            else:
                smoothening = 7 # Slow/Normal movement -> more smoothing

            clocX = plocX + (x_mapped - plocX) / smoothening
            clocY = plocY + (y_mapped - plocY) / smoothening

            # 7. Move Mouse
            try:
                pyautogui.moveTo(wScr - clocX, clocY)
            except pyautogui.FailSafeException:
                pass 
            
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # 8. Both Index and Middle Fingers are up : Left Clicking Mode
        # Ensure Ring finger is DOWN to avoid conflict with Scroll/Right Click
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0:
            # 9. Find distance between fingers
            length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            # print(length)

            # 10. Click mouse if distance is short
            if length < 40:
                cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click()
        
        # 11. Middle and Ring Fingers are up : Right Clicking Mode
        # Ensure Pinky is DOWN
        if fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
            length = ((x3 - x2) ** 2 + (y3 - y2) ** 2) ** 0.5
            
            if length < 40:
                cv2.circle(img, (x2, y2), 15, (0, 0, 255), cv2.FILLED) # Red for Right Click
                pyautogui.rightClick()

        # 12. Thumb and Index Fingers are up : Volume Control Mode
        # Only Thumb and Index should be up (Middle down)
        if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0:
            length = ((x1 - x4) ** 2 + (y1 - y4) ** 2) ** 0.5
            
            # Draw visual feedback
            cv2.line(img, (x4, y4), (x1, y1), (255, 0, 255), 3)
            cx, cy = (x1 + x4) // 2, (y1 + y4) // 2
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            # Map length (range ~50 to 300) to Volume (0 to 100)
            vol = np.interp(length, [50, 250], [0, 100])
            
            # Set Volume (MacOS)
            os.system(f"osascript -e 'set volume output volume {int(vol)}'")
            
            cv2.putText(img, f'{int(vol)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 3)

        # 13. All Fingers Up : Scroll Mode
        if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
            # Use y-position of Middle Finger to scroll
            # If hand is in top part of screen -> Scroll Up
            # If hand is in bottom part -> Scroll Down
            # Or use relative movement? Relative is better but tricky without state.
            # Let's use Position-based Scrolling (like a joystick).
            
            # Middle finger y (y2)
            # Center of screen is hCam / 2
            # Dead zone in middle
            
            scroll_threshold = 50
            mid_y = hCam // 2
            
            if y2 < mid_y - scroll_threshold:
                pyautogui.scroll(10) # Scroll Up
                cv2.putText(img, "Scroll UP", (20, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            elif y2 > mid_y + scroll_threshold:
                pyautogui.scroll(-10) # Scroll Down
                cv2.putText(img, "Scroll DOWN", (20, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    # 11. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # 12. Display
    # Draw the boundary box for movement range
    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
    
    cv2.imshow("Virtual Mouse", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
