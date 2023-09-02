import paho.mqtt.client as mqtt
import json
import random
import time
from datetime import datetime

# broker settings

broker_host = "192.168.1.3"
broker_port = 1883

# create client
client = mqtt.Client()

# connection

client.connect(broker_host, broker_port)


# make list for ids

sensor_ids = ["sensor1","sensor2","sensor3"]


while True:
    for sensor_id in sensor_ids:
        readings = round(random.uniform(0,100),2)
        timestamp = datetime.utcnow().isoformat()


        payload = {
            "sensor_id":sensor_id,
            "value":readings,
            "timestamp":timestamp


        }
        topic = f"sensor/{sensor_id}"
        client.publish(topic, json.dumps(payload))

        print(f"Published to the topic'{topic}': {payload}")

        time.sleep(1)
# client disconnection
client.disconnect()