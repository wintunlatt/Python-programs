from pymodbus.client import ModbusTcpClient
import time

# Modbus server details
IP_ADDRESS = '192.168.1.11'
PORT = 502  # Default Modbus TCP port
CONTROL_COIL_ADDRESS = 17  # Coil to ON/OFF based on user input

def write_coil(client, address, value):
    try:
        result = client.write_coil(address, value)
        if result.isError():
            print(f"Error writing to coil {address}")
        else:
            state = "ON" if value else "OFF"
            print(f"Coil {address} turned {state}")
    except Exception as e:
        print(f"Exception while writing: {e}")

def main():
    client = ModbusTcpClient(IP_ADDRESS, port=PORT)
    if client.connect():
        print("Connected to Modbus server.")

        try:
            while True:
                user_input = input("Enter 'on' to turn ON or 'off' to turn OFF coil 17 (or 'exit' to quit): ").strip().lower()
                
                if user_input == 'on':
                    write_coil(client, CONTROL_COIL_ADDRESS, True)
                elif user_input == 'off':
                    write_coil(client, CONTROL_COIL_ADDRESS, False)
                elif user_input == 'exit':
                    print("Exiting program.")
                    break
                else:
                    print("Invalid input. Please enter 'on', 'off', or 'exit'.")

                time.sleep(2)  # Wait 2 seconds before next prompt

        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
        finally:
            client.close()
            print("Connection closed.")
    else:
        print("Unable to connect to Modbus server.")

if __name__ == "__main__":
    main()
