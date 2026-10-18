import unittest
import math
from Orbit_math import Satellite_param


class TestSatelliteParam(unittest.TestCase):

    def test_400_km_orbit(self):
        r, v, T = Satellite_param(400)
        self.assertAlmostEqual(r, 6771, places=3)
        self.assertAlmostEqual(v, 7.6726, places=3)
        self.assertAlmostEqual(T, 92.4142, places=2)
    def test_800_km_orbit(self):
        r, v, T = Satellite_param(800)
        self.assertAlmostEqual(r, 7171, places=3)
        self.assertAlmostEqual(v, 7.454, places=2)
        self.assertAlmostEqual(T, 100.7231, places=2)
    def test_higher_orbit(self):
        r1, v1, T1 = Satellite_param(400)
        r2, v2, T2 = Satellite_param(800)

        self.assertGreater(r2, r1)
        self.assertLess(v2, v1)
        self.assertGreater(T2, T1)

    def test_invalid_altitudes(self):
        for alt in [0, -10, "400", True, float("nan"),
                    float("inf"), -float("inf")]:
            with self.subTest(alt=alt):
                with self.assertRaises(ValueError):
                    Satellite_param(alt)


if __name__ == "__main__":
    unittest.main()
