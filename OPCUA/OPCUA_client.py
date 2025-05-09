from opcua import Client
import time

url = "opc.tcp://localhost:4840/freeopcua/server/"
client = Client(url)

try:
    client.connect()
    print("Client connected to OPC UA Server")

    # Get objects node
    objects_node = client.get_objects_node()

    # Browse children of Objects node
    children = objects_node.get_children()

    # Find "Device1"
    device_node = None
    for child in children:
        if child.get_browse_name().Name == "Device1":
            device_node = child
            break

    if device_node is None:
        raise Exception("Device1 node not found")

    # Now find variables under Device1
    variables = device_node.get_children()
    digital_node = None
    analog_node = None

    for var in variables:
        name = var.get_browse_name().Name
        if name == "DigitalInput":
            digital_node = var
        elif name == "AnalogValue":
            analog_node = var

    if not digital_node or not analog_node:
        raise Exception("DigitalInput or AnalogValue not found")

    while True:
        digital_value = digital_node.get_value()
        analog_value = analog_node.get_value()
        print(f"Digital: {digital_value}, Analog: {analog_value}")
        time.sleep(1)

except Exception as e:
    print("Error:", e)

finally:
    client.disconnect()
    print("Client disconnected")
