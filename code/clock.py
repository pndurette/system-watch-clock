from math import cos, radians, sin

from displayio import Group
from vectorio import Polygon


class ClockHand(Group):
    def __init__(
        self,
        x: int,
        y: int,
        length: int,
        width: int,
        angle: int,
        pixel_shader,
        color_index: int = 0,
    ):
        """
        The hand of a clock

        A shape (vectorio.Polygon in a displayio Group) representing
        a clock hand: a rectangle with a <length> and a <width> tilted
        at clockwise <angle> degrees around (<x>,<y>):

                   +------length-----+
                   |                 | width
               - - + - * (x,y) - - - + - - - angle
                   |                 |         v
                   +-----------------+
                   |<->|
                    width/2

        Args:
            x: The x-axis coordinate of the rotation point
            y: The y-axis coordinate of the rotation point
            length: The lenght of the hand, in pixels
            width: The width (thickness) of the hand, in pixels
            angle: The angle of rotation around (x,y), in degrees
            pixel_shader: The pixel_shader, as expected by vectorio
            color_index: The color_index, as expected by vectorio
        """
        super().__init__()
        self._angle = angle
        self._initial_points = []

        # Calculate points of hand shape (relative to 0,0)
        self._initial_points = self._calculate_points(length=length, width=width)

        # Apply rotation in-place
        rotated_points = self._rotate(self._initial_points, angle)

        # Create Polygon from rotated points and place at x,y
        _polygon = Polygon(
            pixel_shader=pixel_shader,
            points=rotated_points,
            x=x,
            y=y,
            color_index=color_index,
        )

        # Append to self (Group)
        self.append(_polygon)

    def _calculate_points(self, length: int, width: int):
        """
        Calculate the 4-point coordinates of the clock hand

        The rectangle with its centre of rotation at (0,0)
        which is an offset of half the width from the centre-left
        of the shape:

           (x0,y0)                    (x1,y1)
                   +------length-----+
                   |                 |
                   |   * (0,0)       width
                   |                 |
                   +-----------------+
           (x3,y3) |<->|              (x2,y2)
                    width/2

        Args:
            length: The lenght of the hand, in pixels
            width: The width (thickness) of the hand, in pixels

        Returns:
            The list of points (tuples) to create the rectangle
        """
        x0, y0 = 0 - width / 2,          0 + width / 2  # fmt: skip
        x1, y1 = 0 - width / 2 + length, 0 + width / 2
        x2, y2 = 0 - width / 2 + length, 0 - width / 2
        x3, y3 = 0 - width / 2,          0 - width / 2  # fmt: skip

        # Points as vectorio.Polygon expects
        # i.e (List[Tuple[int,int]])
        points = [(x0, y0), (x1, y1), (x2, y2), (x3, y3)]
        print(f"debug: {self} (initial) {points}")
        return points

    def _rotate(self, points, angle: int):
        """
        Rotate a series of points around (0,0)

        Args:
            points: The list of points (tuples) to rotate
            angle: The angle of rotation around (0,0), in degrees
        """
        angle_rad = radians(angle)

        # Rotation transformation matrix, i.e:
        # x' = x * cos(angle_rad) - y * sin(angle_rad)
        # y' = x * sin(angle_rad) + y * cos(angle_rad)
        x_prime = lambda x, y, angle: int(x * cos(angle_rad) - y * sin(angle_rad))
        y_prime = lambda x, y, angle: int(x * sin(angle_rad) + y * cos(angle_rad))

        # Apply rotation to all (x,y) points
        new_points = [(x_prime(x, y, angle), y_prime(x, y, angle)) for (x, y) in points]
        print(f"debug: {self} ({angle}º) {new_points}")
        return new_points

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, new_angle):
        # Rotate the initial points
        new_points = self._rotate(self._initial_points, new_angle)

        # Group (self) only has the Polygon, refresh its points
        self[0].points = new_points
