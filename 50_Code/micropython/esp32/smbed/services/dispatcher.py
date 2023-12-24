from collections import deque

class Event:
  pass

class Dispatcher:  
  event_queue: deque[Event]

  def __init__(self) -> None:
    self.event_queue = deque((), 20, 1)

  def register_event_type(self, event_cls, handler):
    pass

  def dispatch(self, event: Event) -> None:
    try:
      self.event_queue.append(event)
    except IndexError as e:
      pass

  async def process_queue(self):
    print("Process events")