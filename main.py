import cv2
from ultralytics import YOLO
import pyttsx3
import time

# Initialize Text-to-Speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)

# Load YOLOv8x model (most accurate)
model = YOLO("yolov8x.pt")

# Start webcam
cap = cv2.VideoCapture(0)

# Set resolution (HD)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

spoken_objects = set()
last_spoken_time = time.time()
speak_interval = 5  # seconds
confidence_threshold = 0.4  # Only consider predictions above this confidence

print("🎥 AI Assistant is running with YOLOv8x... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Perform object detection
    results = model(frame)[0]

    # Store currently detected object labels
    current_objects = []
    for box in results.boxes:
        if box.conf[0] < confidence_threshold:
            continue
        cls_id = int(box.cls[0])
        label = model.names[cls_id]
        current_objects.append(label)

    # Annotate and display the frame
    annotated_frame = results.plot()
    cv2.imshow("AI Assistant - Object Detection", annotated_frame)

    # Speak new objects or at intervals
    current_time = time.time()
    if current_objects:
        unique_objects = set(current_objects)
        new_objects = unique_objects - spoken_objects
        if new_objects or (current_time - last_spoken_time) > speak_interval:
            text = "I see: " + ", ".join(unique_objects)
            print("🔊 " + text)
            engine.say(text)
            engine.runAndWait()
            spoken_objects = unique_objects
            last_spoken_time = current_time

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
