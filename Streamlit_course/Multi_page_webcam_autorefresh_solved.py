import streamlit as st
import pandas as pd
import numpy as np
from streamlit_autorefresh import st_autorefresh
import cv2
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av

# ✅ Must be first command
st.set_page_config(page_title="Auto-refresh Random Line Chart", layout="centered")
st.title("Main Dashboard")

# Setup tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Home", "Analytics", "Settings", "Multi-page", "Web-cam"])

with tab1:
    st.header("Welcome to Home")
    st.write("This is the home tab.")

    st.title("📈 Live Random Number Line Chart")

    # 📌 Only refresh *inside tab1*
    st_autorefresh(interval=1000, limit=None, key="refresh_home")

    # Initialize session state
    if "data" not in st.session_state:
        st.session_state.data = []

    # Update data
    new_value = np.random.randn()
    st.session_state.data.append(new_value)
    st.session_state.data = st.session_state.data[-50:]

    # Plot the line chart
    df = pd.DataFrame(st.session_state.data, columns=["Random Value"])
    st.line_chart(df)

with tab2:
    st.header("Analytics View")
    st.write("Put your charts and data insights here.")

with tab3:
    st.header("Settings")
    st.write("User preferences or configurations go here.")

with tab4:
    st.header("Multi-page")
    st.write("This is just demo of multiple tabs/pages...")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Column 1")
        st.write("This is the left column.")
        st.button("⏹ Stop")
    with col2:
        st.header("Column 2")
        st.write("This is the 2nd column.")
    with col3:
        st.header("Column 3")
        st.write("This is the 3rd column.")
        st.button("▶️ Start")

with tab5:
    st.title("🎥 Smooth Live Webcam Stream")

    class VideoProcessor(VideoProcessorBase):
        def recv(self, frame):
            img = frame.to_ndarray(format="bgr24")
            
            # (Optional) You can process the frame here
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            return av.VideoFrame.from_ndarray(img, format="rgb24")

    webrtc_streamer(key="example", video_processor_factory=VideoProcessor)
