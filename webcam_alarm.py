import cv2
import time
import winsound
from ultralytics import YOLO

model = YOLO("runs/detect/train/weights/best.pt")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not open webcam")
    exit()

last_alarm_time = 0
ALARM_COOLDOWN = 2

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = model.predict(
        frame,
        conf=0.60,
        verbose=False
    )

    cellphone_detected = False

    for box in results[0].boxes:

        class_id = int(box.cls[0])
        class_name = model.names[class_id]

        if class_name.lower() == "cellphone":
            cellphone_detected = True
            break

    current_time = time.time()

    if cellphone_detected and current_time - last_alarm_time >= ALARM_COOLDOWN:

        print("CELL PHONE DETECTED! ALARM!")

        winsound.PlaySound(
            "alarm.wav",
            winsound.SND_FILENAME | winsound.SND_ASYNC
        )

        last_alarm_time = current_time

    annotated_frame = results[0].plot()

    cv2.imshow("Cellphone Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()