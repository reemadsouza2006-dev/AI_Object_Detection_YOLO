import streamlit as st
from ultralytics import YOLO
from PIL import Image

st.set_page_config(page_title="AI Object Detection", page_icon="🔍")

st.title("🔍 AI Object Detection")
st.write("Upload an image and let YOLO detect objects.")

model = YOLO("yolo11n.pt")

uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file)

    results = model(image, conf=0.5)

    detected_image = results[0].plot()
    detected_image = detected_image[:, :, ::-1]

    st.image(detected_image, caption="Detected Objects")

    object_count = len(results[0].boxes)

    st.success(f"Objects detected: {object_count}")