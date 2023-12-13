import json
import time
from smbed.services import Services
from smbed.daq import OneWireCommunicator

with open('config.json') as f:
    config = json.load(f)

services = Services(config)
services.start()

one_wire = OneWireCommunicator(4)

while True:
    one_wire.read()
    for k, v in one_wire.values.items():    
        services.mqtt.send_sensor_value(str(k), v)
    time.sleep(1)