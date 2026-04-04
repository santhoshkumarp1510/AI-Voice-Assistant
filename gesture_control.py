import cv2
import pyautogui
import numpy as np

pyautogui.FAILSAFE = False
screen_width, screen_height = pyautogui.size()

def run_gesture_control():
    try:
        import mediapipe as mp
        from mediapipe.tasks import python as mp_python
        from mediapipe.tasks.python import vision
        from mediapipe.tasks.python.vision import HandLandmarkerOptions
    except Exception as e:
        print(f"MediaPipe import error: {e}")
        return

    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Camera not available.")
        return

    print("Gesture control running. Press ESC to stop.")

    # Download model if not exists
    import os
    import urllib.request
    model_path = "hand_landmarker.task"
    if not os.path.exists(model_path):
        print("Downloading hand landmarker model...")
        url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
        urllib.request.urlretrieve(url, model_path)
        print("Model downloaded.")

    base_options = mp_python.BaseOptions(model_asset_path=model_path)
    options = HandLandmarkerOptions(
        base_options=base_options,
        num_hands=1
    )
    landmarker = vision.HandLandmarker.create_from_options(options)

    while True:
        ret, frame = camera.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )
        result = landmarker.detect(mp_image)

        if result.hand_landmarks:
            landmarks = result.hand_landmarks[0]

            tips = [8, 12, 16, 20]
            fingers = []
            for tip in tips:
                if landmarks[tip].y < landmarks[tip - 2].y:
                    fingers.append(True)
                else:
                    fingers.append(False)

            index_x = landmarks[8].x
            index_y = landmarks[8].y
            mouse_x = int(index_x * screen_width)
            mouse_y = int(index_y * screen_height)

            if all(fingers):
                pyautogui.moveTo(mouse_x, mouse_y, duration=0.05)
                cv2.putText(frame, "MOVE", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            elif fingers[0] and not any(fingers[1:]):
                pyautogui.click()
                cv2.putText(frame, "CLICK", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            elif fingers[0] and fingers[1] and not fingers[2] and not fingers[3]:
                if index_y < 0.4:
                    pyautogui.scroll(3)
                    cv2.putText(frame, "SCROLL UP", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                else:
                    pyautogui.scroll(-3)
                    cv2.putText(frame, "SCROLL DOWN", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        cv2.imshow("Gesture Control (ESC to stop)", frame)
        if cv2.waitKey(1) == 27:
            break

    landmarker.close()
    camera.release()
    cv2.destroyAllWindows()