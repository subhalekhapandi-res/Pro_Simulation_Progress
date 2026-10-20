
import math as m


class Es_param_find:
    R = 6371
    GM = 3.986005 * 10**14
    M = 5.9742 * 10**24

    def __init__(self, alt):
        if (
            isinstance(alt, bool)
            or not isinstance(alt, (int, float))
            or not m.isfinite(alt)
            or alt <= 0
        ):
            raise ValueError("Invalid Altitude")

        self.h = alt
        self.orbit_rad = self.R + self.h
        self.velocity = (self.GM * 10**-9 / self.orbit_rad)**0.5
        self.orbit_period = (
            2 * m.pi * ((self.orbit_rad * 10**3)**3 / self.GM)**0.5
        )
        self.a_velocity = 2 * m.pi / self.orbit_period
        self.now_t = 0
        self.elaps_t = 0
        self.a_pos = 0
        self.coor_pos = (self.orbit_rad, 0)

    def simulate(self, t):
        if (
            isinstance(t, bool)
            or not isinstance(t, (int, float))
            or not m.isfinite(t)
            or t < 0
        ):
            raise ValueError("Invalid Time")

        self.now_t = t
        self.elaps_t = t % self.orbit_period
        self.a_pos = self.a_velocity * self.elaps_t

        self.coor_pos = (
            self.orbit_rad * m.cos(self.a_pos),
            self.orbit_rad * m.sin(self.a_pos)
        )

        return self.coor_pos

    def trajectory(self, step_t):
        if (
            isinstance(step_t, bool)
            or not isinstance(step_t, (int, float))
            or not m.isfinite(step_t)
            or step_t <= 0
            or step_t > self.orbit_period
        ):
            raise ValueError("Invalid Step Time")

        points = []
        t = 0

        while t < self.orbit_period:
            points.append(self.simulate(t))
            t += step_t

        points.append(self.simulate(self.orbit_period))
        return points

    def orbit_completed(self, elapsed_time):
        if (
            isinstance(elapsed_time, bool)
            or not isinstance(elapsed_time, (int, float))
            or not m.isfinite(elapsed_time)
            or elapsed_time < 0
        ):
            raise ValueError("Invalid Time")

        return elapsed_time >= self.orbit_period

    def completed_orbits(self, elapsed_time):
        if (
            isinstance(elapsed_time, bool)
            or not isinstance(elapsed_time, (int, float))
            or not m.isfinite(elapsed_time)
            or elapsed_time < 0
        ):
            raise ValueError("Invalid Time")

        return int(elapsed_time // self.orbit_period)

    def altitude_status(self, threshold):
        if (
            isinstance(threshold, bool)
            or not isinstance(threshold, (int, float))
            or not m.isfinite(threshold)
            or threshold <= 0
        ):
            raise ValueError("Invalid Altitude Threshold")

        if self.h >= threshold:
            return "THRESHOLD REACHED"

        return "NORMAL"

    def safety_check(self, min_alt, max_alt, min_speed, max_speed):
        limits = (min_alt, max_alt, min_speed, max_speed)

        if any(
            isinstance(v, bool)
            or not isinstance(v, (int, float))
            or not m.isfinite(v)
            for v in limits
        ):
            raise ValueError("Invalid Safety Limits")

        if min_alt > max_alt or min_speed > max_speed:
            raise ValueError("Invalid Safety Limits")

        if self.h < min_alt or self.h > max_alt:
            return "ALTITUDE WARNING"

        if self.velocity < min_speed or self.velocity > max_speed:
            return "SPEED WARNING"

        return "NORMAL"


if __name__ == "__main__":
    sat = Es_param_find(400)
    T = sat.orbit_period

    print("Completed orbits:")
    print(sat.completed_orbits(0))
    print(sat.completed_orbits(T - 1))
    print(sat.completed_orbits(T))
    print(sat.completed_orbits(2 * T))

    print("\nOther checks:")
    print(sat.orbit_completed(T))
    print(sat.altitude_status(300))
    print(sat.altitude_status(500))
    print(sat.safety_check(300, 500, 7, 9))
