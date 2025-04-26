import streamlit as st
st.set_page_config(page_title="Digital I/O Dashboard", layout="centered")

import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import mysql.connector

# --------- MySQL Config ---------
db_config = {
    "host": "localhost",
    "user": "root",      # ← Replace with your MySQL user
    "password": "wintunlatt123",  # ← Replace with your MySQL password
    "database": "OEE_dashboard"
}

def insert_log(total_on_time, start_time, stop_time):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        sql = "INSERT INTO Machine_status (sensor, start_time, stop_time) VALUES (%s, %s, %s)"
        cursor.execute(sql, (total_on_time, start_time, stop_time))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Database error: {e}")

# --------- Auto-refresh every 1 second ---------
st_autorefresh(interval=1000, key="refresh")

# --------- Initialize session state ---------
if 'logging' not in st.session_state:
    st.session_state.logging = False
if 'digital_button' not in st.session_state:
    st.session_state.digital_button = False
if 'log_df' not in st.session_state:
    st.session_state.log_df = pd.DataFrame(columns=['Time', 'Status'])
if 'on_time_df' not in st.session_state:
    st.session_state.on_time_df = pd.DataFrame(columns=['Time', 'ON_Time'])
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'stop_time' not in st.session_state:
    st.session_state.stop_time = None
if 'total_on_time' not in st.session_state:
    st.session_state.total_on_time = 0
if 'last_log_time' not in st.session_state:
    st.session_state.last_log_time = datetime.now()

# --------- Title ---------
st.title("🖥️ Machine Control Dashboard")

# --------- Start / Stop Buttons ---------
col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Start"):
        st.session_state.logging = True
        st.session_state.start_time = datetime.now()
        st.session_state.total_on_time = 0
        st.session_state.log_df = pd.DataFrame(columns=['Time', 'Status'])
        st.session_state.on_time_df = pd.DataFrame(columns=['Time', 'ON_Time'])
with col2:
    if st.button("⏹ Stop"):
        st.session_state.logging = False
        st.session_state.stop_time = datetime.now()
        if st.session_state.start_time:
            insert_log(
                total_on_time=st.session_state.total_on_time,
                start_time=st.session_state.start_time,
                stop_time=st.session_state.stop_time
            )

st.markdown(f"**Status:** {'🟢 Running' if st.session_state.logging else '🔴 Stopped'}")

# --------- Digital Button + Indicator Lamp ---------
st.subheader("🔘 Digital Input Simulation")
col3, col4 = st.columns(2)

with col3:
    digital_pressed = st.toggle("Press Digital Button", value=st.session_state.digital_button)
    st.session_state.digital_button = digital_pressed

with col4:
    if st.session_state.digital_button:
        st.markdown("#### 💡 Indicator: 🟢 ON")
    else:
        st.markdown("#### 💡 Indicator: 🔴 OFF")

# --------- Real-time Logging and ON Time Calculation ---------
now = datetime.now()
elapsed = (now - st.session_state.last_log_time).total_seconds()
st.session_state.last_log_time = now

if st.session_state.logging:
    if st.session_state.digital_button:
        st.session_state.total_on_time += elapsed

    # Log current button state
    new_data = pd.DataFrame([[now.strftime("%H:%M:%S"), int(st.session_state.digital_button)]],
                            columns=['Time', 'Status'])
    st.session_state.log_df = pd.concat([st.session_state.log_df, new_data], ignore_index=True)

    # Update accumulated ON time for plotting
    st.session_state.on_time_df = pd.concat([
        st.session_state.on_time_df,
        pd.DataFrame([[now.strftime("%H:%M:%S"), st.session_state.total_on_time]],
                     columns=['Time', 'ON_Time'])
    ], ignore_index=True)

# --------- Time Series Plot ---------
if not st.session_state.log_df.empty:
    st.subheader("📈 Digital Button Status Over Time")
    chart_data = st.session_state.log_df.copy()
    chart_data['Status'] = chart_data['Status'].astype(int)
    st.line_chart(data=chart_data.set_index('Time'))

# --------- Real-time ON Time Plot ---------
if not st.session_state.on_time_df.empty:
    st.subheader("📊 Accumulated ON Time (seconds)")
    st.line_chart(data=st.session_state.on_time_df.set_index('Time'))

# --------- Show Total ON Time ---------
if st.session_state.logging or st.session_state.total_on_time > 0:
    st.subheader("⏱️ Digital Button ON Time")
    st.write(f"**{round(st.session_state.total_on_time, 1)} seconds**")
