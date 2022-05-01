import json
from random import random, uniform
from time import sleep, time

import paho.mqtt.client as mqtt


def main():
    # Setup MQTT client and connect
    client = mqtt.Client(client_id="main")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("ubidots-balena", 1883, 60)
    client.loop_start()

    while True:
        timestamp = int(1000 * time())

        # Send data to device
        topic = "/"
        payload = {
            "humidity": {
                "value": round(uniform(50, 52), 0),
                "timestamp": timestamp,
            },
            "pressure": {
                "value": round(uniform(95, 105), 1),
                "timestamp": timestamp,
            },
        }
        print(f"[INFO] Send data to device\n{topic}: {payload}")
        client.publish(topic, json.dumps(payload))

        # Send data to variable
        topic = "temperature"
        payload = {"value": round(uniform(25, 30), 1), "timestamp": timestamp}
        print(f"[INFO] Send data to variable\n{topic}: {payload}")
        client.publish(topic, json.dumps(payload))

        sleep(10)


def on_connect(client, userdata, flags, rc):
    print(f"[INFO] Connected with result code {rc}")

    # Subscribe to variable last value
    client.subscribe("humidity/lv")

    # Subscribe to variable last dot
    client.subscribe("temperature")


def on_message(client, userdata, msg):
    print(
        f"[INFO] Receive data from variable\n{msg.topic}: {msg.payload.decode()}"
    )


if __name__ == "__main__":
    main()
