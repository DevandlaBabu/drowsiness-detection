# 🚗 DriveGuard AI: Real-Time Driver Fatigue Monitoring System

A real-time AI-based Driver Drowsiness Detection System using **Python, OpenCV, and MediaPipe**.  
The system detects **eye closure, yawning, and fatigue**, and sends **voice alerts, alarms, and Telegram notifications with GPS location**.

---

## 📌 Features

- 👁️ Real-time Eye Drowsiness Detection (EAR method)
- 😮 Yawning Detection (MAR method)
- ⏱️ Timer-based accuracy (reduces false alerts)
- 🔊 Voice Alert using pyttsx3
- 🚨 Alarm sound for emergency warning
- 📊 Drowsiness counting system
- 📱 Telegram alerts to multiple users
- 🌍 GPS location sharing (IP-based)
- 📝 Logging system (stores events in log.txt)

---

## 🛠️ Technologies Used

- Python
- OpenCV
- MediaPipe Face Mesh
- NumPy
- pyttsx3 (Voice Engine)
- playsound
- requests (Telegram API + GPS API)

---

## 📷 System Workflow

Camera → Face Detection → MediaPipe Landmarks →
EAR (Eye Aspect Ratio) + MAR (Mouth Aspect Ratio) →
Decision (Drowsy / Yawning) →
Alerts (Voice + Alarm + Telegram + GPS)
## 🧠 Working Principle

### 👁️ Eye Detection (EAR)
- Detects eye closure using facial landmarks
- If EAR is low → eyes are closed → drowsiness detected

### 😮 Yawning Detection (MAR)
- Detects mouth opening
- If MAR is high → yawning detected

### ⏱️ Timer Logic
- Condition must persist for a few seconds
- Prevents false detection

---

## 📱 Telegram Alert System

- Uses Telegram Bot API
- Sends alerts to all registered users
- Includes driver name + GPS location

---

## 🌍 GPS Feature

- Uses IP-based location tracking (`ipinfo.io`)
- Sends:
  - City
  - Region
  - Country
  - Google Maps link

---

## 📂 Project Structure
driver-drowsiness/
│
├── app.py
├── alarm.mp3
├── log.txt
├── README.md
└── requirements.txt


---

## 📦 Installation

```bash
pip install opencv-python mediapipe numpy pyttsx3 playsound requests

##🚀 Run Project:
python app.py

📊 Output Example:
Drowsy Alert: "Wake up!"
Yawning Alert: "You are yawning"

##Telegram Message:
⚠️ DRIVER DROWSINESS ALERT
Name: Ravi
Status: Drowsy
Location: Hyderabad, India

🎯 Applications
🚗 Driver safety systems
🚌 Bus / Truck monitoring
🚕 Taxi driver alert systems
🚓 Fleet management safety

## Future Improvements:
Mobile app integration 📱
AI deep learning model upgrade 🤖
Live cloud dashboard 🌐
Real-time GPS tracking 🚗

👨‍💻 Author:

Developed by: Bogiredy Obulreddy(Final Year AI/ML)

⚠️ Disclaimer:
This project uses IP-based location and webcam data only for educational purposes.

# mysql connecting
1.pip install mysql-connector-python
2.pip show mysql-connector-python


##)
🎯 FINAL FLOW diagram :

Telegram user → send message
        ↓
Save in MySQL database
        ↓
Drowsiness detected
        ↓
Fetch all users from DB
        ↓
Send alert to all

#logic of ear and mar
#cv2.putText(frame, f"EAR: {ear:.2f}", (300, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) 
#cv2.putText(frame, f"MAR: {mar:.2f}", (300, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
