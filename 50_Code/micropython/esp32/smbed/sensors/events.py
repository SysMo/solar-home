from ..scheduler import Event
from dataclasses import dataclass

class SensorReadingFloat(Event):
  def __init__(self, id: str, value: float, timestamp = None):
    self.id = id
    self.value = value
    self.timestamp = timestamp
