import streamlit as st
import cv2

st.title("🎥 Live Webcam Video Stream")

# Start/Stop checkbox — correctly assign a key
start_camera = st.checkbox('Start Camera', key="start_camera")

# Open the webcam
if start_camera:
    cap = cv2.VideoCapture(0)
    frame_placeholder = st.empty()

    while st.session_state.start_camera:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture video.")
            break

        # Convert to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(frame, channels="RGB")

    cap.release()
