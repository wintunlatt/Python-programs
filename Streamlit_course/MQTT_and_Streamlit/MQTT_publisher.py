# mqtt_publisher.py
import paho.mqtt.client as mqtt
import random
import time

broker = "test.mosquitto.org"
port = 1883
topic = "Win/MQTT_test/num"

client = mqtt.Client()

client.connect(broker, port)

try:
    while True:
        value = random.randint(1, 100)
        client.publish(topic, str(value))
        print(f"Published: {value}")
        time.sleep(5)
except KeyboardInterrupt:
    print("Stopped by user")
    client.disconnect()
