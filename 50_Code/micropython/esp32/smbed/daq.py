
import machine, onewire, ds18x20, time

class OneWireCommunicator:
  pin: int
  values: dict

  def __init__(self, pin: int):
    self.pin = pin
    ds_pin = machine.Pin(4)
    self.one_wire = onewire.OneWire(ds_pin)
    self.ds_array = ds18x20.DS18X20(self.one_wire)
    self.values = {}
  
  def read(self):
    sensor_b = self.ds_array.scan()
    sensor_ids = [int.from_bytes(x, 'big') for x in sensor_b]
    self.ds_array.convert_temp()
    time.sleep_ms(750)
    for i in range(len(sensor_b)):
      self.values[sensor_ids[i]] = self.ds_array.read_temp(sensor_b[i])
  


    
    
