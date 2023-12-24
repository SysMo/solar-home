from ..scheduler import Event

class ServiceMessage(Event):
  def __init__(self, msg):
    self.msg = msg