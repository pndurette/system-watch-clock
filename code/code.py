import time
import board
import displayio
import vectorio
from math import sin, cos, pi

from clock import ClockHand

# Add a light to see (on the Magtag)
import neopixel

pixels = neopixel.NeoPixel(board.NEOPIXEL, 4, brightness=0.1)
pixels[0] = (255, 255, 255)
pixels[1] = (255, 255, 255)
pixels[2] = (255, 255, 255)
pixels[3] = (255, 255, 255)

# "Pixel" size (for the hands) in real pixels
pixel_size = 20

# use built in display (PyPortal, PyGamer, PyBadge, CLUE, etc.)
display = board.DISPLAY

# Rotate display
display.rotation = 0

# Make and show the display context
main_group = displayio.Group()
display.show(main_group)

# Make a background color fill
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
main_group.append(bg_sprite)

# Fill Colour
_palette = displayio.Palette(1)
_palette[0] = 0x0  # Black

hand = ClockHand(
    x=int(display.width / 2),
    y=int(display.height / 2),
    length=pixel_size * 3,
    width=pixel_size,
    angle=0,  # HOUR_RAD * 12 - OFFSET_RAD,
    pixel_shader=_palette,
)
main_group.append(hand)

hand.angle = 45
hand.angle = 90

# Do refresh after it's okay for the ePaper (plus an arbitrary wait)
time.sleep(display.time_to_refresh + 0.2)
display.refresh()

while True:
    pass
