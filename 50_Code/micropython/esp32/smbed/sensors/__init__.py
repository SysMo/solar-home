from .one_wire import OneWireCommunicator

class SensorManager:
  def __init__(self, sensor_communicators):
    self.sensor_communicators = sensor_communicators

  @staticmethod
  def from_config(data) -> SensorManager:
    sensor_communicators = {}
    for sensor_id, sensor_definition in data.items():
      if isinstance(sensor_definition, dict) and len(list(sensor_definition)) == 1:
        for iface_type, iface_config in sensor_definition.items():
          if iface_type == "OneWire":
            try:
              sensor_communicators[sensor_id] = \
                OneWireCommunicator.from_config(iface_config)
              
            except ValueError as e:
              print(e)
          else:
            print(f"Unknown sensor type {iface_type}")
      else:
        print("Sensor interface definition should be a map with a single entry: {interface_type: interface_definition}")
        print(sensor_definition)
    return SensorManager(sensor_communicators)


