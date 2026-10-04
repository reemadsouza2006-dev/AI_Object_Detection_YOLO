import streamlit as st
import cv2
from ultralytics import YOLO
import tempfile


st.set_page_config(
    page_title="AI Object Detection & Tracking",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Object Detection & Tracking")
st.write(
    "Real-time object detection and multi-object tracking "
    "powered by YOLO."
)

st.divider()

uploaded_file = st.file_uploader(
    "Upload an image or video",
    type=["jpg", "jpeg", "png", "mp4", "avi", "mov"]
)

confidence = st.slider(
    "Detection Confidence",
    0.1,
    1.0,
    0.5,
    0.05
)

if uploaded_file:

    model = YOLO("yolo11n.pt")

    file_type = uploaded_file.type

    if file_type.startswith("image"):

        file_bytes = uploaded_file.read()

        image = cv2.imdecode(
            __import__("numpy").frombuffer(
                file_bytes,
                dtype="uint8"
            ),
            cv2.IMREAD_COLOR
        )

        results = model.track(
            image,
            persist=True,
            conf=confidence
        )

        annotated = results[0].plot()

        st.image(
            cv2.cvtColor(
                annotated,
                cv2.COLOR_BGR2RGB
            ),
            caption="Detected Objects",
            use_container_width=True
        )

        st.success(
            f"Objects detected: {len(results[0].boxes)}"
        )

    else:

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp4"
        )

        temp_file.write(
            uploaded_file.read()
        )

        temp_file.close()

        cap = cv2.VideoCapture(
            temp_file.name
        )

        frame_placeholder = st.empty()

        while cap.isOpened():

            success, frame = cap.read()

            if not success:
                break

            results = model.track(
                frame,
                persist=True,
                conf=confidence
            )

            annotated = results[0].plot()

            frame_placeholder.image(
                cv2.cvtColor(
                    annotated,
                    cv2.COLOR_BGR2RGB
                ),
                channels="RGB"
            )

        cap.release()

        st.success(
            "Video processing completed."
        )

else:

    st.info(
        "Upload an image or video to begin detection and tracking."
    )