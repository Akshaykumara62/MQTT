import paho.mqtt.client as mqtt
import json
import redis

# MQTT broker settings
broker_address = "192.168.1.3"  # Replace with your MQTT broker's address
broker_port = 1883  # Default MQTT port

# Create an MQTT client
client = mqtt.Client()

# Connect to the MQTT broker
client.connect(broker_address, broker_port)

# Create a Redis connection
redis_client = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)

# Callback when a message is received
def on_message(client, userdata, message):
    payload = json.loads(message.payload.decode("utf-8"))

    # Store the reading in Redis using a list data structure
    sensor_id = payload["sensor_id"]
    reading = json.dumps(payload)
    redis_key = f"latest_readings:{sensor_id}"

    # Trim the list to store only the latest ten readings
    redis_client.lpush(redis_key, reading)
    redis_client.ltrim(redis_key, 0, 9)

    print(f"Received and stored message in Redis: {payload}")

# Set the MQTT callback
client.on_message = on_message

# Subscribe to MQTT topics
topics = ["sensors/temperature", "sensors/humidity"]
for topic in topics:
    client.subscribe(topic)
    print(f"Subscribed to topic '{topic}'")

# Start the MQTT loop
client.loop_forever()
