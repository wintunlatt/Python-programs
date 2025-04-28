from pymodbus.client import ModbusTcpClient
import time

# Modbus server details
IP_ADDRESS = '192.168.1.11'
PORT = 502  # Default Modbus TCP port
COIL_ADDRESS = 1  # Coil address to read

def read_coil(client, address):
    try:
        result = client.read_coils(address, count=1)
        if result.isError():
            print(f"Error reading coil {address}")
        else:
            print(f"Coil {address} state: {result.bits[0]}")
    except Exception as e:
        print(f"Exception: {e}")

def main():
    client = ModbusTcpClient(IP_ADDRESS, port=PORT)
    if client.connect():
        print("Connected to Modbus server.")
        try:
            while True:
                read_coil(client, COIL_ADDRESS)
                time.sleep(2)
        except KeyboardInterrupt:
            print("Program stopped by user.")
        finally:
            client.close()
            print("Connection closed.")
    else:
        print("Unable to connect to Modbus server.")

if __name__ == "__main__":
    main()
