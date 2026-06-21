# ===================== IMPORTS =====================
import cv2
import time
import mediapipe as mp
import numpy as np
import threading
import pyttsx3
import requests
import mysql.connector
import pygame
#from playsound import playsound

# ===================== VOICE =====================
engine = pyttsx3.init()

# ===================== MEDIA PIPE =====================
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

# ===================== LANDMARKS =====================
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
MOUTH = [13, 14, 78, 308]

# ===================== MYSQL =====================
#db = mysql.connector.connect(
   # host="localhost",
    #user="root",
   # password="online",
    #database="drowsiness_db"
#)
#cursor = db.cursor()

# ===================== TELEGRAM =====================
TOKEN = "urs token here"


# ===================== VARIABLES =====================
drowsy_count = 0
eye_start_time = None
yawn_start_time = None

voice_on = False
yawn_voice_on = False

alarm_on = False
last_alarm_time = 0

# ===================== FUNCTIONS =====================

def speak(text):
    engine.say(text)
    engine.runAndWait()

def alarm():
    global alarm_on

    if not pygame.mixer.get_init():
        pygame.mixer.init()

    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("alarm.wav")
        pygame.mixer.music.play(-1)   # continuous loop
        alarm_on = True

def stop_alarm():
    global alarm_on

    if pygame.mixer.get_init():
        pygame.mixer.music.stop()

    alarm_on = False

#def alarm():


 #   playsound("alarm.wav")

def save_log(msg):
    with open("log.txt", "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {msg}\n")

def get_location():
    try:
        res = requests.get("https://ipinfo.io/json")
        data = res.json()
        loc = data.get("loc", "")
        city = data.get("city", "")
        region = data.get("region", "")
        country = data.get("country", "")

        return f"{city}, {region}, {country}\nhttps://maps.google.com/?q={loc}"
    except:
        return "Location not available"

def send_alert_all():
    location = get_location()

    #cursor.execute("SELECT chat_id, first_name FROM users")
    #users = cursor.fetchall()

    for chat_id, name in users:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

        message = f"""⚠️ DRIVER DROWSINESS ALERT

👤 Name: {name}
🚨 Status: Drowsy detected
📍 Location:
{location}
"""

        requests.post(url, data={"chat_id": chat_id, "text": message})

# ===================== CAMERA =====================
cap = cv2.VideoCapture(0)

EAR_THRESHOLD = 0.25
MAR_THRESHOLD = 0.4

EYE_TIME = 2
YAWN_TIME = 2

# ===================== MAIN LOOP =====================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:

        for face_landmarks in results.multi_face_landmarks:

            # ========== EYE ==========
            left_eye = []
            right_eye = []

            for i in LEFT_EYE:
                x = int(face_landmarks.landmark[i].x * w)
                y = int(face_landmarks.landmark[i].y * h)
                left_eye.append([x, y])

            for i in RIGHT_EYE:
                x = int(face_landmarks.landmark[i].x * w)
                y = int(face_landmarks.landmark[i].y * h)
                right_eye.append([x, y])

            left_eye = np.array(left_eye)
            right_eye = np.array(right_eye)

            A = np.linalg.norm(left_eye[1] - left_eye[5])
            B = np.linalg.norm(left_eye[2] - left_eye[4])
            C = np.linalg.norm(left_eye[0] - left_eye[3])
            ear = (A + B) / (2.0 * C)

            # ========== MOUTH ==========
            mouth = []
            for i in MOUTH:
                x = int(face_landmarks.landmark[i].x * w)
                y = int(face_landmarks.landmark[i].y * h)
                mouth.append([x, y])

            mouth = np.array(mouth)

            vertical = np.linalg.norm(mouth[0] - mouth[1])
            horizontal = np.linalg.norm(mouth[2] - mouth[3])
            mar = vertical / horizontal

            # ===================== YAWN TIMER =====================
            if mar > MAR_THRESHOLD:
                if yawn_start_time is None:
                    yawn_start_time = time.time()

                elif time.time() - yawn_start_time > YAWN_TIME:
                    cv2.putText(frame, "YAWNING!", (50, 150),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

                    if not yawn_voice_on:
                        threading.Thread(target=speak, args=("You are yawning",)).start()
                        save_log("Yawning detected")
                        yawn_voice_on = True
            else:
                yawn_start_time = None
                yawn_voice_on = False

            # ===================== DROWSY TIMER =====================
        

            if ear < EAR_THRESHOLD:

                if eye_start_time is None:
                    eye_start_time = time.time()

                elif time.time() - eye_start_time > EYE_TIME:

                    cv2.putText(frame, "DROWSY!", (50, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

                    if time.time() - last_alarm_time > 3:

                        drowsy_count += 1

                        # START ALARM
                        if not alarm_on:
                            threading.Thread(target=alarm).start()

                        # SPEAK ONLY ONCE
                        if not voice_on:
                            threading.Thread(
                                target=speak,
                                args=("Wake up! You are drowsy",)
                            ).start()

                            voice_on = True

                        save_log(f"Drowsy count {drowsy_count}")

                        if drowsy_count >= 5:
                            send_alert_all()

                        last_alarm_time = time.time()

            else:
                eye_start_time = None
                voice_on = False

                # STOP ALARM WHEN NORMAL
                if alarm_on:
                    stop_alarm()
 

            # ===================== DISPLAY =====================
            cv2.putText(frame, f"EAR: {ear:.2f}", (300, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            cv2.putText(frame, f"MAR: {mar:.2f}", (300, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            cv2.putText(frame, f"DROWSY COUNT: {drowsy_count}", (50, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow("Drowsiness Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
#RESULT
#👁️ Drowsy detected → alert
#😮 Yawning → voice alert
#TIMER LOGIC 2sec
#VOICE +ALARAM ALERT
#📊 Log saved
#📱 100 users → each gets message with their name
#?📱 Send GPS location:IP GEOLOCATION (WIFI / IP)
#You now have:

# ✔ Voice alert → pyttsx3
# ✔ Alarm sound → pygame
#Drowsiness detection → MediaPipe
# ✔ Telegram alert → API


