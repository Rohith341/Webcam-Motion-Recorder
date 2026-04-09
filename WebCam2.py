import cv2
import numpy as np
import time
import os
import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# ✅ Authenticate Google Drive
def authenticate_drive():
    gauth = GoogleAuth()
    try:
        gauth.LoadClientConfigFile("C:/Users/rohit/Documents/SEM---3-2/py_project/client_secrets.json")
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)
        print("✅ Google Drive Authentication Successful!")
        return drive
    except Exception as e:
        print(f"❌ Google Authentication Failed: {e}")
        return None

drive = authenticate_drive()
if not drive:
    exit("🚨 Exiting: Google Authentication failed!")

# 🔹 Create folder for video storage
SAVE_PATH = "recordings"
os.makedirs(SAVE_PATH, exist_ok=True)

# 🔹 Video Capture Setup with Higher Quality
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height
fourcc = cv2.VideoWriter_fourcc(*"MJPG")  # Better codec for quality
motion_detected = False
recording = False
motion_start_time = 0
RECORD_TIME = 20  # Seconds

# 🔹 Background subtraction
fgbg = cv2.createBackgroundSubtractorMOG2()

def upload_to_drive(file_path):
    """Uploads video to Google Drive and confirms upload success."""
    if not os.path.exists(file_path):
        print(f"⚠️ File '{file_path}' not found for upload.")
        return

    try:
        file = drive.CreateFile({'title': os.path.basename(file_path)})
        file.SetContentFile(file_path)
        file.Upload()
        print(f"📤 File uploaded to Google Drive: {file_path}")

        # Verify upload
        file_list = drive.ListFile({'q': f"title = '{os.path.basename(file_path)}'"}).GetList()
        if file_list:
            print(f"✅ Upload Verified: {file_list[0]['title']} (ID: {file_list[0]['id']})")
        else:
            print(f"⚠️ Upload Error: File not found in Drive!")

    except Exception as e:
        print(f"❌ Upload Failed: {e}")

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Error: Failed to capture frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (15, 15), 0)
    fgmask = fgbg.apply(blur)

    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detected = False
    for contour in contours:
        if cv2.contourArea(contour) > 800:  # Lower sensitivity for better accuracy
            detected = True
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "MOTION!", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

    # 🔹 Start recording when motion is detected
    if detected and not recording:
        recording = True
        motion_detected = True
        motion_start_time = time.time()
        video_filename = os.path.join(SAVE_PATH, f"motion_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.avi")
        out = cv2.VideoWriter(video_filename, fourcc, 20.0, (1280, 720))
        print(f"🎥 Motion detected! Recording started: {video_filename}")

    # 🔹 Continue recording for 20 seconds after last motion
    if recording:
        out.write(frame)
        if time.time() - motion_start_time > RECORD_TIME and not detected:
            recording = False
            out.release()
            print(f"✅ Recording saved: {video_filename}")

            # 🔹 Upload to Google Drive
            upload_to_drive(video_filename)

    # 🔹 UI Enhancements
    date_time_text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 🟥 Slim Red Border if Motion is Detected
    if detected:
        cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), 4)

    # 🏷️ Display Motion Status
    status_text = "MOTION DETECTED" if detected else "NO MOTION"
    status_color = (0, 0, 255) if detected else (0, 255, 0)

    # 🔹 Semi-transparent background for status
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (200, 40), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

    # 🔹 Display Status with Smaller Font
    cv2.putText(frame, status_text, (15, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 1)

    # 🔹 Display Date & Time
    cv2.putText(frame, date_time_text, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    # 🔹 Show Live Feed
    cv2.imshow("Motion Detector", frame)

    # 🔹 Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
