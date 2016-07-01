import unittest
from imagefudge.image_fudge import Fudged

TEST_IMAGE = 'examples/GodRoss.jpg'

class TestFudged(unittest.TestCase):
    def setUp(self):
        self.fudge = Fudged(TEST_IMAGE)

    def tearDown(self):
        self.fudge.image.close()

    def test_get_center(self):
        center = self.fudge.get_center()
        assert(center.x == self.fudge.width/2)
        assert(center.y == self.fudge.height/2)

if __name__ == "__main__":
    unittest.main()

