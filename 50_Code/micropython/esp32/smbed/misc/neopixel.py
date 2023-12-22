import machine
import neopixel
import math
import time

np = neopixel.NeoPixel(machine.Pin(8), 1)
i = 0
A = 32
while True:
  r = round(A * (1 + math.sin(i / 10)) / 2)
  g = round(A * (1 + math.sin(i / 10 + math.pi * 2 / 3)) / 2 )
  b = round(A * (1 + math.sin(i / 10 + math.pi * 4 / 3)) / 2)
  np[0] = (r, g, b)
  np.write()
  i += 1
  i = i % 628
  time.sleep_ms(50)
