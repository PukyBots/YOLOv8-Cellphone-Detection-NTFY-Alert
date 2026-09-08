import cv2
import requests
import winsound
from ultralytics import YOLO


# =============================
# LOAD YOLO MODEL
# =============================

model = YOLO("runs/detect/train/weights/best.pt")


# =============================
# OPEN CAMERA
# =============================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not open webcam")
    exit()


# =============================
# NTFY CONFIGURATION
# =============================

NTFY_TOPIC = "pulkit-cellphone-alert"
NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"


# =============================
# ALARM CONFIGURATION
# =============================

ALARM_FILE = "alarm.wav"


# Prevent repeated notifications/alarm
alert_sent = False


# =============================
# NTFY FUNCTION
# =============================

def send_ntfy(message):

    try:

        response = requests.post(
            NTFY_URL,
            data=message.encode("utf-8"),
            headers={
                "Title": "Cellphone Detected",
                "Priority": "high",
                "Tags": "warning"
            },
            timeout=10
        )

        if response.status_code == 200:

            print("ntfy notification sent")

        else:

            print("ntfy error:", response.status_code)

    except Exception as e:

        print("ntfy connection failed:", e)


# =============================
# MAIN LOOP
# =============================

while True:

    ret, frame = cap.read()

    if not ret:
        print("Failed to read camera frame")
        break


    # =============================
    # YOLO DETECTION
    # =============================

    results = model.predict(
        frame,
        conf=0.80,
        verbose=False
    )


    # Draw detections
    annotated_frame = results[0].plot()


    # =============================
    # CHECK FOR CELLPHONE
    # =============================

    cellphone_detected = False

    for box in results[0].boxes:

        class_id = int(box.cls[0])

        class_name = model.names[class_id]

        print("Detected:", class_name)

        if class_name.lower() == "cellphone":

            cellphone_detected = True

            break


    # =============================
    # SEND ALERT
    # =============================

    if cellphone_detected and not alert_sent:

        print("================================")
        print("CELL PHONE DETECTED!")
        print("Sending notification...")
        print("Playing alarm...")
        print("================================")


        # -------- NTFY --------
        send_ntfy(
            "Cellphone usage detected by the camera."
        )


        # -------- ALARM --------
        winsound.PlaySound(
            ALARM_FILE,
            winsound.SND_FILENAME | winsound.SND_ASYNC
        )


        # Prevent repeated alerts
        alert_sent = True


    # =============================
    # RESET ALERT
    # =============================

    # Once the cellphone disappears,
    # another alert can be generated
    if not cellphone_detected:

        alert_sent = False


    # =============================
    # DISPLAY
    # =============================

    cv2.imshow(
        "Cellphone Detection",
        annotated_frame
    )


    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# =============================
# CLEANUP
# =============================

cap.release()
cv2.destroyAllWindows()

winsound.PlaySound(None, winsound.SND_PURGE)