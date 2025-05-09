# opcua_server.py
from opcua import Server
from datetime import datetime
import random
import time

# Setup server
server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
server.set_server_name("Demo OPC UA Server")

# Create a namespace
uri = "http://examples.org"
idx = server.register_namespace(uri)

# Create an object to hold variables
objects = server.get_objects_node()
myobj = objects.add_object(idx, "Device1")

# Add variables: one digital (bool), one analog (float)
digital = myobj.add_variable(idx, "DigitalInput", True)
analog = myobj.add_variable(idx, "AnalogValue", 0.0)

# Allow variables to be writable
digital.set_writable()
analog.set_writable()

# Start server
server.start()
print("OPC UA Server started at opc.tcp://0.0.0.0:4840/freeopcua/server/")

try:
    while True:
        # Update variable values
        digital.set_value(random.choice([True, False]))
        analog.set_value(round(random.uniform(0, 100), 2))
        time.sleep(1)

except KeyboardInterrupt:
    print("Shutting down server.")
    server.stop()
