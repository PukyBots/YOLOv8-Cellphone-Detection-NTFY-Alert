import cv2
from ultralytics import YOLO

model = YOLO("runs/detect/train/weights/best.pt")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not open webcam")
    exit()

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = model.predict(
        frame,
        conf=0.40,
        verbose=False
    )

    annotated_frame = results[0].plot()

    cv2.imshow(
        "Cellphone Detection",
        annotated_frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()