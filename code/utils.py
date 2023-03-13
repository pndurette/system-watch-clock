import board
import neopixel

PIXEL_COUNT = 4  # MagTag
PIXELS = neopixel.NeoPixel(board.NEOPIXEL, PIXEL_COUNT, brightness=0.1)


def lights(on: bool):
    # Turn on some lights during dev!
    if on:
        for p in range(0, PIXEL_COUNT):
            PIXELS[p] = (255, 255, 255)  # White
    else:
        for p in range(0, PIXEL_COUNT):
            PIXELS[p] = (0, 0, 0)  # Off
