def lights(on=True):
    # Turn on some lights during dev!
    # (Magtag has 4 neopixels)
    if on:
        import board
        import neopixel

        pixels = neopixel.NeoPixel(board.NEOPIXEL, 4, brightness=0.1)
        pixels[0] = (255, 255, 255)
        pixels[1] = (255, 255, 255)
        pixels[2] = (255, 255, 255)
        pixels[3] = (255, 255, 255)
    else:
        pixels = neopixel.NeoPixel(board.NEOPIXEL, 4, brightness=0)
