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
    hours=12,
    minutes=15,
    pixel_shader=clock_palette,
)

# Add to group
main_group.append(clock)

# Do refresh after it's okay for the ePaper (plus an arbitrary wait)
time.sleep(display.time_to_refresh + 0.2)
display.refresh()

while True:
    pass
