import streamlit as st
from pymodbus.client import ModbusTcpClient

# Modbus server details
IP_ADDRESS = '192.168.1.11'
PORT = 502  # Default Modbus TCP port

# Coil addresses
COIL1_ADDRESS = 16
COIL2_ADDRESS = 17

# Set up Modbus client
client = ModbusTcpClient(IP_ADDRESS, port=PORT)

def write_coil(address, value):
    try:
        if client.connect():
            result = client.write_coil(address, value)
            client.close()
            if result.isError():
                st.error(f"Error writing to coil {address}")
            else:
                state = "ON" if value else "OFF"
                st.success(f"Coil {address} turned {state}")
        else:
            st.error("Failed to connect to Modbus server.")
    except Exception as e:
        st.error(f"Exception while writing: {e}")

# Streamlit Dashboard
st.set_page_config(page_title="WISE-4012E Coil Control", layout="centered")
st.title("WISE-4012E Modbus Coil Control Dashboard")

st.subheader("Control Coil 1 (Address 16)")
col1, col2 = st.columns(2)
with col1:
    if st.button('Turn ON Coil 1', use_container_width=True):
        write_coil(COIL1_ADDRESS, True)
with col2:
    if st.button('Turn OFF Coil 1', use_container_width=True):
        write_coil(COIL1_ADDRESS, False)

st.subheader("Control Coil 2 (Address 17)")
col3, col4 = st.columns(2)
with col3:
    if st.button('Turn ON Coil 2', use_container_width=True):
        write_coil(COIL2_ADDRESS, True)
with col4:
    if st.button('Turn OFF Coil 2', use_container_width=True):
        write_coil(COIL2_ADDRESS, False)
