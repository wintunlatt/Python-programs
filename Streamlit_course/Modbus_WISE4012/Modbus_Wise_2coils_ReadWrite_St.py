import streamlit as st
from pymodbus.client import ModbusTcpClient
import time

# Modbus server details
IP_ADDRESS = '192.168.1.11'
PORT = 502  # Default Modbus TCP port

# Coil addresses for writing
COIL1_ADDRESS = 16
COIL2_ADDRESS = 17

# Coil addresses for reading (inputs)
INPUT1_ADDRESS = 0
INPUT2_ADDRESS = 1

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

def read_coil(address):
    try:
        if client.connect():
            result = client.read_coils(address, count=1)
            client.close()
            if result.isError():
                return None
            return result.bits[0]
        else:
            return None
    except Exception as e:
        return None

def main():
    # Reading coil states (Inputs 0 and 1)
    input1_state = read_coil(INPUT1_ADDRESS)
    input2_state = read_coil(INPUT2_ADDRESS)

    # Control Coil 1
    st.subheader("Control Coil 1 (Address 16)")
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Turn ON Coil 1', use_container_width=True):
            write_coil(COIL1_ADDRESS, True)
    with col2:
        if st.button('Turn OFF Coil 1', use_container_width=True):
            write_coil(COIL1_ADDRESS, False)

    # Control Coil 2
    st.subheader("Control Coil 2 (Address 17)")
    col3, col4 = st.columns(2)
    with col3:
        if st.button('Turn ON Coil 2', use_container_width=True):
            write_coil(COIL2_ADDRESS, True)
    with col4:
        if st.button('Turn OFF Coil 2', use_container_width=True):
            write_coil(COIL2_ADDRESS, False)

    # Show Coil Input Status
    st.subheader("Coil Input Status (Read-Back)")

    if input1_state is not None:
        st.info(f"Coil 0 Status: {'ON' if input1_state else 'OFF'}")
    else:
        st.error("Failed to read Coil 0")

    if input2_state is not None:
        st.info(f"Coil 1 Status: {'ON' if input2_state else 'OFF'}")
    else:
        st.error("Failed to read Coil 1")


    # Refresh the page every 2 seconds
    time.sleep(2)
    st.rerun()  # This should replace st.experimental_rerun()


if __name__ == "__main__":
    main()
