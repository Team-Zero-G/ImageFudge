import math
import ntpath
import os
from random import random, randrange
from PIL import Image
from PIL import ImageDraw

from collections import namedtuple


class FudgeUtils(object):

    Point = namedtuple('Point', ['x', 'y'])

    def __init__(self, image, scale=2):

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

        return self.Point(int(random()*self.width),
                          int(random()*self.height))

    def get_center(self):

        return self.Point(x=self.width/2, y=self.height/2)

    def save(self, path):

        self.image.thumbnail((self.width//self.scale, self.height//self.scale),
                             Image.ANTIALIAS)
        self.image.save(path)

    def random_points(self, point_number):

        for _ in range(point_number):
            yield self.select_point()
