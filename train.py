from ultralytics import YOLO

# Load pretrained YOLO model
model = YOLO("yolov8n.pt")

# Train the model
results = model.train(
    data="dataset/data.yaml",
    epochs=100,
    imgsz=640,
    batch=16,
    patience=20,
    device="cpu"
)

print("Training completed!")