from ultralytics import YOLO

model = YOLO("yolov8n.pt")  

results = model("/home/pi/capture_128.jpg",imgsz=128)

results[0].save() 
#print(results[0].boxes)
