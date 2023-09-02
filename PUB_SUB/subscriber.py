import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient

broker_host = "192.168.1.3"
broker_port = 1883

# creating mongo connection
mongo_host = "localhost"
mongo_port = 27017
mongo_db_name = "sensor_data"
mongo_collection_name = "sensor_readings"

def on_connect(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        client = MongoClient(mongo_host, mongo_port)
        db = client[mongo_db_name]
        collection = db[mongo_collection_name]

        collection.insert_one(payload)
        print(f"Recivied message and stored in mongodb:{payload}")
    except Exception as e:
        print(f"Error", e)

client = mqtt.Client()

client.on_connect = on_connect

client.connect(broker_host, broker_port)

topics = ["sensors/temperature", "sensors/humidity"]
for topic in topics:
    client.subscribe(topic)
    print(f"Subscribed to the topic'{topic}'")

client.loop_forever() 