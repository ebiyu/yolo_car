import cv2

from ultralytics import YOLO

model = YOLO("yolov8n.pt")  

# Open camera
cap = cv2.VideoCapture(0)

# Set video resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while True:
    # Read frame from camera
    ret, frame = cap.read()

    results = model(frame, imgsz=128)

    # results = model(frame)
    boxes = results[0].boxes
    for box in boxes:
        # Check if detected object is a person (class_id 0)
        if box.cls == 0:
            # Get coordinates
            x, y, w, h = box.xywh[0]
            print(f"Person detected at: x={x:.1f}, y={y:.1f}, w={w:.1f}, h={h:.1f}")

    # If frame is not read correctly, break
    if not ret: 
        print("Failed to read frame.")
        break

cap.release()
cv2.destroyAllWindows()
