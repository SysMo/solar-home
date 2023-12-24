
import machine, onewire, ds18x20, time
import binascii
import hashlib
import asyncio

from .communicator import SensorCommunicator

class OneWireCommunicator(SensorCommunicator):
  one_wire: onewire.OneWire
  values: dict

  @classmethod
  def from_config(cls, data):
    return OneWireCommunicator(data["pin"], data["type"])

  def __init__(self, pin: int, sensor_type):
    machine_pin = machine.Pin(pin)
    self.one_wire = onewire.OneWire(machine_pin)
    if sensor_type == "ds18b20":
      self.sensor_array = ds18x20.DS18X20(self.one_wire)
    else:
      raise ValueError(f"Unknown sensor type {sensor_type}")
    self.values = {}
  
  def encode_sensor_id(self, b) -> str:
    return binascii.hexlify(
      hashlib.sha1(b).digest()
    )[:4].decode('utf-8')

  def read(self):
    self.values = {}
    try:
      sensor_b = self.sensor_array.scan()
      sensor_ids = [self.encode_sensor_id(x) for x in sensor_b]
      self.sensor_array.convert_temp()
      time.sleep_ms(750)
      for i in range(len(sensor_b)):
        self.values[sensor_ids[i]] = self.sensor_array.read_temp(sensor_b[i])
    except Exception as e:
      print("Error reading one-wire sensors")

  async def scan_array(self) -> list[bytes]:
    try:
      sensor_raw_ids = self.sensor_array.scan()
      self.sensor_array.convert_temp()
    except Exception as e:
      print("Error scanning one-wire sensors")
    return sensor_raw_ids

  async def read_values(self, sensor_raw_ids: list[bytes]):
    asyncio.sleep_ms(750)
    for raw_id in sensor_raw_ids:
      try:
        id = self.encode_sensor_id(raw_id)
        self.values[id] = self.sensor_array.read_temp(raw_id)
      except Exception as e:
        print("Error reading one-wire value")
    print(self.values)


  async def acquire_data(self):
    raw_ids = await self.scan_array()
    asyncio.create_task(self.read_values(raw_ids))
    

    
