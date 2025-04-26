# Subscriber_Streamlit_DashBd.py
import streamlit as st
import paho.mqtt.client as mqtt
import threading

broker = "test.mosquitto.org"
port = 1883
topic = "Win/MQTT_test/num"

# A shared variable and event to safely update from another thread
latest_value = "Waiting..."
update_event = threading.Event()

def on_connect(client, userdata, flags, rc):
    client.subscribe(topic)

def on_message(client, userdata, msg):
    global latest_value
    latest_value = msg.payload.decode()
    update_event.set()  # Notify Streamlit to update UI

def mqtt_thread():
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port)
    client.loop_forever()

# Start MQTT thread only once
if "mqtt_thread_started" not in st.session_state:
    threading.Thread(target=mqtt_thread, daemon=True).start()
    st.session_state.mqtt_thread_started = True

# Streamlit UI
st.title("Live MQTT Data from Win/MQTT_test/num")

placeholder = st.empty()

# Update UI when event is triggered
while True:
    if update_event.wait(timeout=1):
        placeholder.metric("Received Number", latest_value)
        update_event.clear()
    else:
        placeholder.metric("Received Number", latest_value)
