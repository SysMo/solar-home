from ...protocols.modbus import RegisterMap, RegisterBlock
from ..common import Serializable
from ...protocols.modbus import ModbusType

class DTS777:

  @classmethod
  def register_map(cls):
    return RegisterMap([
      RegisterBlock(name = "BL1", start = 0, len = 27)
        .register(name = "", group = "electrical", start = 0, len = 27, tpe = DTS777Electricity),
      RegisterBlock(name = "BL2", start = 29, len = 52)
        .register(name = "", group = "electrical", start = 29, len = 52, tpe = DTS777Energy),

      # RegisterBlock(name = "", group = "", start = , len = ))
    ])

class DTS777Electricity(ModbusType, Serializable):

  @classmethod
  def from_words(cls, words) -> ModbusType:
    return DTS777Electricity(words)

  def __init__(self, data: list[int]):
    print(f"DTS777Electricity: {len(data)}")
    self.data = data

  @property
  def v1(self) -> float:
    return self.data[0] / 10.0
  @property
  def v2(self) -> float:
    return self.data[1] / 10.0
  @property
  def v3(self) -> float:
    return self.data[2] / 10.0
  
  @property
  def i1(self) -> float:
    return self.data[3] / 10.0
  @property
  def i2(self) -> float:
    return self.data[4] / 10.0
  @property
  def i3(self) -> float:
    return self.data[5] / 10.0

  @property
  def p1(self) -> float:
    return self.data[8]
  @property
  def p2(self) -> float:
    return self.data[9]
  @property
  def p3(self) -> float:
    return self.data[10]

  @property
  def q1(self) -> float:
    return self.data[12]
  @property
  def q2(self) -> float:
    return self.data[13]
  @property
  def q3(self) -> float:
    return self.data[14]

  @property
  def pf1(self) -> float:
    return self.data[20] / 1000.0
  @property
  def pf2(self) -> float:
    return self.data[21] / 1000.0
  @property
  def pf3(self) -> float:
    return self.data[22] / 1000.0

  @property
  def f(self) -> float:
    return self.data[26] / 100.0

  def serialize(self) -> object:
    return {
      "v1": self.v1,
      "v2": self.v2,
      "v3": self.v3,
      "i1": self.i1,
      "i2": self.i2,
      "i3": self.i3,
      "p1": self.p1,
      "p2": self.p2,
      "p3": self.p3,
      "pf1": self.pf1,
      "pf2": self.pf2,
      "pf3": self.pf3,
      "f": self.f,
    }
  
  def __str__(self):
    return str(self.serialize)
  
class DTS777Energy(ModbusType, Serializable):
  def __init__(self, data: list[int]):
    self.data = data

  @classmethod
  def from_words(cls, words) -> ModbusType:
    return DTS777Energy(words)

  def serialize(self) -> object:
    return {
    }