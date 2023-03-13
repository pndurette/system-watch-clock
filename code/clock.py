from math import cos, radians, sin

from displayio import Group
from vectorio import Circle, Polygon, Rectangle


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
               - - * (x,y) - - - - - + - - - angle
                   |                 |         v
                   +-----------------+

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
        Calculate the 4-point initial coordinates of the clock hand

        The rectangle with its centre of rotation at (0,0)
        which is on centre-left edge of the shape:

           (x0,y0)                    (x1,y1)
                   +------length-----+
                   |                 |
                   * (0,0)           width
                   |                 |
                   +-----------------+
           (x3,y3)                   (x2,y2)

        Args:
            length: The lenght of the hand, in pixels
            width: The width (thickness) of the hand, in pixels

        Returns:
            The list of points (tuples) to create the rectangle
        """
        x0, y0 = 0,          0 + width / 2  # fmt: skip
        x1, y1 = 0 + length, 0 + width / 2
        x2, y2 = 0 + length, 0 - width / 2
        x3, y3 = 0,          0 - width / 2  # fmt: skip

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

    @property
    def points(self):
        # Group (self) only has the Polygon, get its points
        return self[0].points


class Clock(Group):
    def __init__(
        self,
        x: int,
        y: int,
        hours: int,
        minutes: int,
        pixel_shader,
        color_index: int = 0,
    ):
        """
        A minimalist clock

        Two ClockHands in a displayio Group representing to display time
        plus an endcap (vectorio.Polygon) to join the two ClockHands
        neatly in their centre.

        Args:
            x: The x-axis coordinate of the rotation point of the clock
            y: The y-axis coordinate of the rotation point of the clock
            hours: The initial time (hours) to show
            minutes: The initial time (minutes) to show
            pixel_shader: The pixel_shader, as expected by vectorio
            color_index: The color_index, as expected by vectorio
        """
        super().__init__()
        self._minutes = minutes
        self._hours = hours

        # Create ClockHand for the hours
        self._hours_hand = ClockHand(
            x=x,
            y=y,
            length=20 * 3,
            width=20,
            angle=self._hours_to_degrees(hours),
            pixel_shader=pixel_shader,
            color_index=color_index,
        )

        # Create ClockHand for the minutes
        self._minutes_hand = ClockHand(
            x=x,
            y=y,
            length=20 * 4,
            width=20,
            angle=self._minutes_to_degrees(minutes),
            pixel_shader=pixel_shader,
            color_index=color_index,
        )

        # Create an endcap Polygon to join
        # the hands neatly in the middle
        _endcap_points = self._calculate_endcap_points(
            self._hours_hand.points, self._minutes_hand.points
        )
        self._endcap = Polygon(
            pixel_shader=pixel_shader, points=_endcap_points, x=x, y=y
        )

        # TODO: Manage the indices better
        self.append(self._hours_hand)  # 0
        self.append(self._minutes_hand)  # 1
        self.append(self._endcap)  # 2

    def _calculate_endcap_points(self, hours_hand_points, minutes_hand_points):
        """
        Calculate the 4-point coordinates of the shape joining the centre
        endpoints of the two hands (i.e. (x0,y0) and (x3,y3) of each)

        Args:
            hours_hand_points: List of point tuples of the hours hand shape
            minutes_hand_points: List of point tuples of the minutes hand shape

        Returns:
            List of point tuples to display a Polygon to fill the gap
        """
        hours_p0, _, _, hours_p3 = hours_hand_points
        min_p0, _, _, min_p3 = minutes_hand_points
        return [hours_p0, min_p0, hours_p3, min_p3]

    def _minutes_to_degrees(self, minutes: int):
        # 6 degrees per minute (i.e 360/60)
        # Minus 90 degrees offset (0 degrees is on the x-axis)
        return minutes * 6 - 90

    def _hours_to_degrees(self, hours: int):
        # 30 degrees per hour (i.e 360/12)
        # Minus 90 degrees offset (0 degrees is on the x-axis)
        return hours * 30 - 90

    @property
    def hours(self):
        return self.hours

    @hours.setter
    def hours(self, new_hours: int):
        # Update hours
        self._hours = new_hours
        print(f"debug: {self} (hours) {new_hours}")

        # Update hours clockhand
        self[0].angle = self._hours_to_degrees(new_hours)

        # Update endcap
        self[2].points = self._calculate_endcap_points(self[0].points, self[1].points)

    @property
    def minutes(self):
        return self._minutes

    @minutes.setter
    def minutes(self, new_minutes: int):
        # Update minutes
        self._minutes = new_minutes
        print(f"debug: {self} (minutes) {new_minutes}")

        # Update minutes clockhand
        self[1].angle = self._minutes_to_degrees(new_minutes)

        # Update endcap
        self[2].points = self._calculate_endcap_points(self[0].points, self[1].points)
