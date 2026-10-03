import cv2
from ultralytics import YOLO

print("Starting AI Object Detection...")

# Load YOLO model
model = YOLO("yolo11n.pt")

# Confidence threshold
confidence = 0.5

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Webcam could not be opened.")
    input("Press Enter to close...")
    exit()

print("Webcam started successfully!")
print("Press Q to quit.")

while True:
    success, frame = cap.read()

    if not success:
        print("ERROR: Could not read webcam frame.")
        break

    # Detect objects
    results = model(frame, conf=confidence)

    # Draw detection boxes
    annotated_frame = results[0].plot()

    # Count detected objects
    object_count = len(results[0].boxes)

    # Show object count
    cv2.putText(
        annotated_frame,
        f"Objects Detected: {object_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # Display result
    cv2.imshow("AI Object Detection", annotated_frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print("Object detection stopped.")