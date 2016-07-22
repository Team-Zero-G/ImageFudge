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

    def __init__(self, image):
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

        self.width = self.image.size[0]
        self.height = self.image.size[1]

    @staticmethod
    def anti_alias(scale=2):
        def anti_alias_dec(method):
            """anti aliasing decortator"""
            def antia(self, *args):
                width = self.image.size[0]*scale
                height = self.image.size[1]*scale
                self.image = self.image.resize((width, height))
                method(self, *args)
                self.image = self.image.resize((width//scale,
                                                height//scale),
                                               Image.ANTIALIAS)
            return antia
        return anti_alias_dec


    def select_point(self):
        """ Returns a random point in the image """
        return self.Point(int(random()*self.image.size[0]),
                          int(random()*self.image.size[1]))

    def get_center(self):
        """ Returns the center point of the image """
        return self.Point(x=self.image.size[0]/2, y=self.image.size[1]/2)

    def save(self, path):
        """ Scales the image back down with antialiasing and saves it """
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
