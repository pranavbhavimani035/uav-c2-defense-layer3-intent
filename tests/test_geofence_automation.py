import unittest

from geofence.geofence import is_inside_geofence


class TestGeofenceAutomation(unittest.TestCase):

    def setUp(self):
        # Rectangular geofence configuration
        self.geofence = {
            "min_x": 0,
            "max_x": 100,
            "min_y": 0,
            "max_y": 100
        }

    def test_position_inside_geofence(self):
        result = is_inside_geofence(50, 50, self.geofence)
        self.assertTrue(result)

    def test_position_at_lower_boundary(self):
        result = is_inside_geofence(0, 0, self.geofence)
        self.assertTrue(result)

    def test_position_at_upper_boundary(self):
        result = is_inside_geofence(100, 100, self.geofence)
        self.assertTrue(result)

    def test_position_beyond_upper_boundary(self):
        result = is_inside_geofence(101, 50, self.geofence)
        self.assertFalse(result)

    def test_position_beyond_lower_boundary(self):
        result = is_inside_geofence(-1, 50, self.geofence)
        self.assertFalse(result)

    def test_position_outside_y_boundary(self):
        result = is_inside_geofence(50, 101, self.geofence)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
    