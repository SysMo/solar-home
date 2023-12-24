import network
import ntptime
import utime
import machine

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
        print("Syncing time ...")
        ntptime.settime()
        print(rtc.datetime())