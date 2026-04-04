import cv2
import face_recognition
import os
import numpy as np

def load_known_faces(folder="known_faces"):
    known_encodings = []
    known_names = []
    if not os.path.exists(folder):
        os.makedirs(folder)
        return known_encodings, known_names
    for filename in os.listdir(folder):
        if filename.endswith((".jpg", ".png")):
            image_path = os.path.join(folder, filename)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(os.path.splitext(filename)[0])
    return known_encodings, known_names

def register_face(name):
    os.makedirs("known_faces", exist_ok=True)
    camera = cv2.VideoCapture(0)
    print(f"Registering face for: {name}")
    print("Look at the camera. Press SPACE to capture.")
    while True:
        ret, frame = camera.read()
        cv2.imshow("Register Face - Press SPACE to capture", frame)
        key = cv2.waitKey(1)
        if key == 32:
            save_path = f"known_faces/{name}.jpg"
            cv2.imwrite(save_path, frame)
            print(f"Face saved as {save_path}")
            break
        elif key == 27:
            break
    camera.release()
    cv2.destroyAllWindows()

def authenticate_user():
    known_encodings, known_names = load_known_faces()
    if not known_encodings:
        print("No registered faces found. Skipping face auth.")
        return True
    camera = cv2.VideoCapture(0)
    print("Face authentication started. Look at the camera...")
    authenticated = False
    attempts = 0
    max_attempts = 100
    while attempts < max_attempts:
        ret, frame = camera.read()
        if not ret:
            break
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        for encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, encoding, tolerance=0.5)
            distances = face_recognition.face_distance(known_encodings, encoding)
            if True in matches:
                best_match = np.argmin(distances)
                name = known_names[best_match]
                print(f"✅ Authenticated: {name}")
                authenticated = True
                break
        if authenticated:
            break
        cv2.imshow("Face Authentication", frame)
        if cv2.waitKey(1) == 27:
            break
        attempts += 1
    camera.release()
    cv2.destroyAllWindows()
    return authenticated