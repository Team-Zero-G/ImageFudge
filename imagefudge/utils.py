import math
import ntpath
import os
from random import random, randrange
from PIL import Image
from PIL import ImageDraw

from collections import namedtuple


class FudgeUtils(object):
    """ Image Fudge helper class """

    Point = namedtuple('Point', ['x', 'y'])

    def __init__(self, image, scale=2):
        """ Opens the image and scales it for antialiasing """
        try:
            self.image = Image.open(image)
        except TypeError as e:
            try:
                if image.__name__ == 'PIL.Image':
                    self.image = image
                else: raise e
            except AttributeError:
                raise e

        self.scale = scale
        self.width = self.image.size[0]*self.scale
        self.height = self.image.size[1]*self.scale
        self.image = self.image.resize((self.width, self.height))

    def select_point(self):
        """ Returns a random point in the image """
        return self.Point(int(random()*self.width),
                          int(random()*self.height))

    def get_center(self):
        """ Returns the center point of the image """
        return self.Point(x=self.width/2, y=self.height/2)

    def save(self, path):
        """ Scales the image back down with antialiasing and saves it """
        self.image = self.image.resize((self.width//self.scale, self.height//self.scale),
                                       Image.ANTIALIAS)
        self.image.save(path)

    def random_points(self, point_number):
        """ Yeilds a number of random points in the image """
        for _ in range(point_number):
            yield self.select_point()

    @staticmethod
    def make_bounding_box(origin, distance):
        """ Returns 2 points that define a bounding box around an origin """
        return [(origin.x-distance, origin.y-distance),
                (origin.x+distance, origin.y+distance)]

    @staticmethod
    def get_angle(origin, endpoint):
        """ Returns the angle created by the line from origin to endpoint """
        dx = endpoint.x - origin.x
        dy = endpoint.y - origin.y
        return math.degrees(math.atan2(dy, dx))

    @staticmethod
    def get_distance(origin, endpoint):
        """  Returns the distance from one point to another """
        dx = endpoint.x - origin.x
        dy = endpoint.y - origin.y
        return math.floor(math.sqrt(math.pow(dx, 2) + math.pow(dy, 2)))
