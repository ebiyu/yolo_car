import sys

import cv2


from ultralytics import YOLO

if len(sys.argv) != 2:
    print("Usage: python yolo_image.py <image_path>")
    exit(1)

image_path = sys.argv[1]

model = YOLO("yolov8n.pt")

# 画像ファイル名を指定
frame = cv2.imread(image_path)

if frame is None:
    print(f"Failed to read image: {image_path}")
    exit(1)

results = model(frame, imgsz=128)
boxes = results[0].boxes
for box in boxes:
    # Check if detected object is a person (class_id 0)
    if box.cls == 0:
        # Get coordinates
        x, y, w, h = box.xywh[0]
        print(f"Person detected at: x={x:.1f}, y={y:.1f}, w={w:.1f}, h={h:.1f}")
