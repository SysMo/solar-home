import network
import utime
import machine
import ntptime
import json
import time
from umqtt.simple import MQTTClient

class WiFiService:
    def __init__(self, networks):
        self.stored_networks = networks
        self.sta_if = network.WLAN(network.STA_IF)

    @property
    def connected(self) -> bool:
        return self.sta_if.isconnected()
    
    def start(self):
        if self.connected:
            print("Already connected to WiFi")
        else:
            print('Scanning for networks ...')
            self.sta_if.active(True)
            ssid_list = self.sta_if.scan()
            ssid_list = [network[0].decode('UTF-8') for network in ssid_list]
            print(ssid_list)
            for ssid in ssid_list:
                if ssid in self.stored_networks:
                    self.try_connect(ssid, self.stored_networks[ssid])
                    if self.connected:
                        break

        if self.connected:
            print('Network config:', self.sta_if.ifconfig())
            self.sync_time()

    def try_connect(self, ssid, password, timeout = 15):
        print(f"Trying to connect to {ssid} ...")
        t_start = utime.time()
        self.sta_if.connect(ssid, password)
        while utime.time() - t_start < timeout:
            utime.sleep(1)
            if self.sta_if.isconnected():
                print(f"Connected to {ssid}")
                return True
        print(f"Failed to connect to {ssid}")
        return False

    def sync_time(self):
        rtc = machine.RTC()
        print(rtc.datetime())
        print("Syncing time ...")
        ntptime.settime()
        print(rtc.datetime())


class MqttService:
    prefix: str
    def __init__(self, client_id: str, server: str, port: int, user: str, password: str, prefix: str):
        self.client = MQTTClient(
            client_id = client_id,
            server = server,
            port = port,
            user = user,
            password = password
        )
        self.prefix = prefix

    @classmethod
    def from_config(cls, data):
        return MqttService(
            client_id = data["client_id"], 
            server = data["server"], 
            port = data["port"], 
            user = data["user"], 
            password = data["password"], 
            prefix = data["prefix"]
        )

    def start(self):
        self.client.connect()

    def send_sensor_value(self, sensor_id: str, value: float):
        topic = (self.prefix + sensor_id).encode()
        payload = {'timestamp': int(time.time()) + 946677600 + 2 * 3600, 'value': value}
        msg = json.dumps(payload).encode()
        self.client.publish(topic, msg)

class Services:
    def __init__(self, config):
        self.initialized = False
        self.network = WiFiService(config["networks"])
        self.mqtt = MqttService.from_config(config["mqtt"]) 

    def start(self):
        self.network.start()
        self.mqtt.start()
        self.initialized = True

