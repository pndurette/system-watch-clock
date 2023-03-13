import time

import board
import displayio

from clock import Clock
from utils import lights

# Turn on some lights during dev!
lights(True)

# "Pixel" size (for the hands) in real pixels
pixel_size = 20

# use built in display (PyPortal, PyGamer, PyBadge, CLUE, etc.)
display = board.DISPLAY

# Rotate display
display.rotation = 0

# Make and show the display context
main_group = displayio.Group()
display.show(main_group)

# Background color fill
bg_bitmap = displayio.Bitmap(display.width, display.height, 1)
bg_palette = displayio.Palette(1)
bg_palette[0] = 0xFFFFFF  # White
bg_sprite = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette, x=0, y=0)
main_group.append(bg_sprite)

# Clock fill
clock_palette = displayio.Palette(1)
clock_palette[0] = 0x0  # Black

# The clock
clock = Clock(
    x=int(display.width / 2),
    y=int(display.height / 2),
    hours=0,
    minutes=10,
    pixel_shader=clock_palette,
)

# Add to group
main_group.append(clock)

# Do refresh after it's okay for the ePaper (plus an arbitrary wait)
time.sleep(display.time_to_refresh + 0.2)
display.refresh()

# Demo: change time using (MagTag) buttons
import digitalio
from adafruit_debouncer import Debouncer

pin_d11 = digitalio.DigitalInOut(board.D11)
pin_d11.direction = digitalio.Direction.INPUT
pin_d11.pull = digitalio.Pull.UP
hour_plus = Debouncer(pin_d11)

pin_d12 = digitalio.DigitalInOut(board.D12)
pin_d12.direction = digitalio.Direction.INPUT
pin_d12.pull = digitalio.Pull.UP
hour_minus = Debouncer(pin_d12)

pin_d14 = digitalio.DigitalInOut(board.D14)
pin_d14.direction = digitalio.Direction.INPUT
pin_d14.pull = digitalio.Pull.UP
minutes_plus = Debouncer(pin_d14)

pin_d15 = digitalio.DigitalInOut(board.D15)
pin_d15.direction = digitalio.Direction.INPUT
pin_d15.pull = digitalio.Pull.UP
minutes_minus = Debouncer(pin_d15)

while True:
    hour_plus.update()
    hour_minus.update()
    minutes_plus.update()
    minutes_minus.update()

    if hour_plus.fell:
        print("+1h")
        clock.hours += 1

    if hour_minus.fell:
        print("-1h")
        clock.hours -= 1

    if minutes_plus.fell:
        print("+5m")
        clock.minutes += 5

    if minutes_minus.fell:
        print("-5m")
        clock.minutes -= 5

    time.sleep(display.time_to_refresh + 0.2)
    display.refresh()
