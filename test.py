import unittest
from imagefudge.image_fudge import Fudged

TEST_IMAGE = 'examples/GodRoss.jpg'

class TestFudged(unittest.TestCase):
    """
    Tests for the Fudged class and class methods.
    """
    @staticmethod
    def assertPointInImage(point, image):
        assert((point.x < image.width) and (point.y < image.height))

    def setUp(self):
        self.fudge = Fudged(TEST_IMAGE)

    def tearDown(self):
        self.fudge.image.close()

    def test_get_center(self):
        center = self.fudge.get_center()
        assert(center.x == self.fudge.width/2)
        assert(center.y == self.fudge.height/2)

    def test_select_point(self):
        point = self.fudge.select_point()
        self.assertPointInImage(point, self.fudge)

    def test_random_points(self):
        # test 10 random points
        points = self.fudge.random_points(10)
        for point in points:
            self.assertPointInImage(point, self.fudge)


if __name__ == "__main__":
    unittest.main()

