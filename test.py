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
        """
        Checks to ensure the center of the image has the same coordinates
        as the center returned by `get_center`.
        """
        center = self.fudge.get_center()
        assert(center.x == self.fudge.width/2)
        assert(center.y == self.fudge.height/2)

    def test_select_point_in_image(self):
        """
        Checks a single random point to ensure it is within the image
        bounds.
        """
        point = self.fudge.select_point()
        self.assertPointInImage(point, self.fudge)

    def test_ten_random_points(self):
        """
        Tests ten random points to ensure they are all within image
        bounds.
        """
        points = self.fudge.random_points(10)
        for point in points:
            self.assertPointInImage(point, self.fudge)


if __name__ == "__main__":
    unittest.main()
