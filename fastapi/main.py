from fastapi import FastAPI, HTTPException, Query, Path
from typing import List
import redis
import json
import uvicorn

app = FastAPI()

# Create a Redis connection
redis_client = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)

# Endpoint to fetch sensor readings by specifying a start and end range
@app.get("/sensor-readings/")
async def get_sensor_readings(start: int = Query(..., description="Start range (inclusive)"),
                              end: int = Query(..., description="End range (inclusive)")):
    readings = []
    # Assuming sensor readings are stored in Redis
    for i in range(start, end + 1):
        reading = redis_client.lindex("latest_readings:sensor1", i)
        if reading:
            readings.append(json.loads(reading))
    return readings

# Endpoint to retrieve the last ten sensor readings for a specific sensor
@app.get("/sensor-readings/{sensor_id}/last-ten/")
async def get_last_ten_sensor_readings(sensor_id: str = Path(..., description="Sensor ID")):
    readings = []
    # Assuming sensor readings are stored in Redis
    readings = redis_client.lrange(f"latest_readings:{sensor_id}", 0, 9)
    return [json.loads(reading) for reading in readings]

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
