import time
import board
import displayio
import vectorio
from math import sin, cos, pi

# Add a light to see
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
color_palette[0] = 0xFFFFFF
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
main_group.append(bg_sprite)


def hand(x: int, y: int, length: int, width: int, Θ: int) -> vectorio.Polygon:
    """Create a clock hand (a rectangle)

    Args:
        x:
        y:
        length:
        width:
        Θ:

    Returns:
        vectorio.Polygon (with its left side centred at <x>, <y>)
    """
    # Fill Colour
    _palette = displayio.Palette(1)
    _palette[0] = 0x0  # Black

    # Calculate 4-point coordinates of quadrangle
    # * Centre-left (with 1/2 width offset) 'rotation point' at (0, 0)
    # * Lenght of <length> and thickness <width>
    # * Rotation matrix expects Θ aligned with x-axis
    # TODO: Add this to docstring

    #
    # (x0,y0)                   (x1,y1)
    #        +------length-----+
    #        |                 |
    #      - + -*- (x,y) -     width
    #        |                 |
    #        +-----------------+
    # (x3,y3) <-->              (x2,y2)
    #         width/2
    #

    # Initial points
    x0, y0 = x - width / 2, y + width / 2
    x1, y1 = x - width / 2 + length, y + width / 2
    x2, y2 = x - width / 2 + length, y - width / 2
    x3, y3 = x - width / 2, y - width / 2

    # Create list of point tuples, as vectorio.Polygon expects
    points = [(x0, y0), (x1, y1), (x2, y2), (x3, y3)]

    # Debug
    print("Polygon (init)", points)

    # Rotation transformation matrix, i.e:
    # x' = x * cos(Θ) - y * sin(Θ)
    # y' = x * sin(Θ) + y * cos(Θ)
    x_prime = lambda x, y, Θ: int(x * cos(Θ) - y * sin(Θ))
    y_prime = lambda x, y, Θ: int(x * sin(Θ) + y * cos(Θ))

    # Apply rotation to all (x,y) points
    points = [(x_prime(x, y, Θ), y_prime(x, y, Θ)) for (x, y) in points]

    # Debug
    print(f"Polygon ({Θ}º)", points)

    # Create and return the polygon
    # TODO: Take this x, y out (as parameters)
    return vectorio.Polygon(
        pixel_shader=_palette,
        points=points,
        x=int(display.width / 2),
        y=int(display.height / 2),
    )


# TODO: Revisit
# def min_to_rad(min: int) -> int:
#     # 2𝜋 (full circle) * 1/60th (minute) + 𝜋/2 (offset)
#     return (-2 * pi) * (min / 60) - (pi / 2)

# TODO: Revisit
# def hour_to_rad(hour: int) -> int:
#     # 2𝜋 (full circle) * 1/12th (hour) + 𝜋/2 (offset)
#     return (-2 * pi) * (hour / 12) - (pi / 2)


hand_a = hand(
    # TODO: this 0,0 can stay in the function
    x=0,  # int(display.width / 2),
    y=0,  # int(display.height / 2),
    length=pixel_size * 4,
    width=pixel_size,
    Θ=0,
)
main_group.append(hand_a)

# hand_b = hand(
#     x=0,  # int(display.width / 2),
#     y=0,  # int(display.height / 2),
#     length=pixel_size * 3,
#     width=pixel_size,
#     Θ=-pi,
# )
# main_group.append(hand_b)

# Do refresh after it's okay for the ePaper
time.sleep(display.time_to_refresh + 0.2)
display.refresh()

while True:
    pass
