import cv2
from ultralytics import YOLO

print("Starting AI Object Detection and Tracking...")

model = YOLO("yolo11n.pt")

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

    results = model.track(
        frame,
        persist=True,
        conf=0.5
    )

    annotated_frame = results[0].plot()

    object_count = len(results[0].boxes)

    cv2.putText(
        annotated_frame,
        f"Objects Detected: {object_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow(
        "AI Object Detection and Tracking",
        annotated_frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print("Object detection and tracking stopped.")