import streamlit as st
import cv2
import tempfile
import os
import time
import numpy as np
from utils.detector import detect_animals_frame, detect_animals_image

st.set_page_config(page_title="🐾 Animal Detection", layout="wide")

st.title("🐾 Animal Detection System")
st.markdown("Developed by **Anuj Bharti**")

# -------- SIDEBAR --------
st.sidebar.header("Options")

input_type = st.sidebar.radio("Choose Input Type", ("Image", "Video", "Webcam"))

conf = st.sidebar.slider("Detection Confidence", 0.25, 1.00, 0.50)

# 🔥 ALERT TOGGLE BUTTON (UNDER SLIDER)
alerts_on = st.sidebar.checkbox("Enable Alerts 🚨", value=True)

os.makedirs("media/uploads", exist_ok=True)
os.makedirs("media/outputs", exist_ok=True)


# -------- IMAGE --------
def process_image(uploaded_image, conf):
    file_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        st.error("Could not read image")
        return

    result_img, df = detect_animals_image(img, conf)

    output_path = os.path.join("media/outputs", f"{uploaded_image.name}_processed.jpg")
    cv2.imwrite(output_path, result_img)

    st.image(result_img, channels="BGR")
    st.success(f"Saved at: {output_path}")

    if df.empty:
        st.info("No animals detected")
    else:
        st.success(f"🐾 Total Detected: {len(df)}")


# -------- VIDEO --------
def process_video(uploaded_video):
    temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_video.write(uploaded_video.read())

    cap = cv2.VideoCapture(temp_video.name)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    output_path = os.path.join("media/outputs", f"processed_{int(time.time())}.mp4")
    out = cv2.VideoWriter(output_path, fourcc, 25.0,
                          (int(cap.get(3)), int(cap.get(4))))

    frame_display = st.empty()
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % 2 != 0:
            continue

        annotated = detect_animals_frame(frame, conf, alerts_on)
        out.write(annotated)

        frame_display.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))

    cap.release()
    out.release()

    st.video(output_path)


# -------- WEBCAM --------
def process_webcam():
    cap = cv2.VideoCapture(0)
    frame_display = st.empty()

    frame_count = 0

    while st.session_state.get("webcam_running", False):
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % 2 != 0:
            continue

        annotated = detect_animals_frame(frame, conf, alerts_on)
        frame_display.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))

    cap.release()


# -------- MAIN --------
if input_type == "Image":
    img = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    if img:
        process_image(img, conf)

elif input_type == "Video":
    vid = st.file_uploader("Upload Video", type=["mp4"])
    if vid:
        process_video(vid)

elif input_type == "Webcam":

    if "webcam_running" not in st.session_state:
        st.session_state["webcam_running"] = False

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Start Webcam"):
            st.session_state["webcam_running"] = True

    with col2:
        if st.button("Stop Webcam"):
            st.session_state["webcam_running"] = False

    if st.session_state["webcam_running"]:
        process_webcam()
