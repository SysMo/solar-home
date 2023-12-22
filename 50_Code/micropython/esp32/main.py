import json
import time
from smbed.services import Services
from smbed.sensors import SensorManager

with open('config.json') as f:
    config = json.load(f)

services = Services(config)
services.start()

sensor_manager = SensorManager.from_config(config["sensors"])
one_wire = sensor_manager.sensor_communicators["temperature"]

while True:
    one_wire.read()
    for k, v in one_wire.values.items():    
        services.mqtt.send_sensor_value(str(k), v)
    time.sleep(1)