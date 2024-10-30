import json
import machine
import asyncio
import time
import sys
import logging

from .mqtt import MqttService
from .wifi import WiFiService
from .dispatcher import Dispatcher
# from ..sensors import SensorManager

# class RuntimeState:
#     Initilizing = 0
#     ConnectingWiFi = 1
#     SyncingTime = 2
#     ConnectingMQTT = 3

class Runtime:
    # state: RuntimeState
    # sensor_manager: SensorManager
    dispatcher: Dispatcher

    def __init__(self, config):
        logging.info("Starting Morse runtime")
        # self.state = RuntimeState.Initilizing
        self.tick_interval = 2000
        self.dispatcher = Dispatcher()
        self.network = WiFiService(config["networks"])
        self.mqtt = MqttService.from_config(config["mqtt"]) 
        # self.sensor_manager = SensorManager.from_config(config["sensors"], dispatcher = self.dispatcher)

    @staticmethod
    def from_config_file(path: str):
        with open(path) as f:
            config = json.load(f)

        return Runtime(config)

    async def on_start(self):
        self.network.start()
        # self.mqtt.start()
        self.initialized = True

    async def on_tick(self):
        logging.info('Tick')
    #     await self.sensor_manager.acquire_data()
    #     await self.dispatcher.process_queue()

    async def main(self):
        await self.on_start()
        while True:
            # await self.on_tick()
            await asyncio.sleep_ms(self.tick_interval)


    def start(self):
        asyncio.run(self.main())

    def soft_reset(self):
        sys.exit()

    def hard_reset(self):
        machine.reset()


# one_wire = sensor_manager.sensor_communicators["temperature"]

# while True:
#     one_wire.read()
#     for k, v in one_wire.values.items():    
#         services.mqtt.send_sensor_value(str(k), v)
#     time.sleep(1)


# async def main():
#     # while True:
#     #     one_wire.read()
#     #     for k, v in one_wire.values.items():    
#     #         runtime.mqtt.send_sensor_value(str(k), v)
#     #     print(one_wire.values)
#         await asyncio.sleep(1.)

# asyncio.run(main())