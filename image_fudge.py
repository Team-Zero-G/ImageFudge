import math
from random import random
from PIL import Image
from PIL import ImageDraw

from collections import namedtuple

class Fudged(object):
    """ """
    Point = namedtuple('Point', ['x', 'y'])
    Dimention = namedtuple('Dimention', ['width', 'height'])

    def __init__(self, image):
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


    def draw_relative_arcs(self, origin, endpoints):
        if isinstance(endpoints, self.Point):
            endpoints = [endpoints]
        for endpoint in endpoints:
            color = self.image.getpixel(endpoint)
            angle = get_angle(origin, endpoint)
            distance = self.get_distance(origin, endpoint)
            bounding_box = self.make_bounding_box(origin, distance)
            arc = int(random()*360)
            while arc == angle:
                arc = int(random()*360)

            draw = ImageDraw.Draw(self.image).arc(bounding_box,
                                                  angle,
                                                  arc,
                                                  color)

    def select_point(self):
        return self.Point(int(random()*self.width),
                          int(random()*self.height))

    def get_center(self):
        return self.Point(x=self.width/2, y=self.height/2)

    def save(self, path):
        self.image.save(path)

    def random_points(self, point_number):
        for _ in range(point_number):
            yield self.select_point()

    def center_random(self, point_number):
        self.draw_relative_arcs(self.get_center(),
                                self.random_points(point_number))

    @staticmethod
    def make_bounding_box(origin, distance):
        return [(origin.x-distance, origin.y-distance),
                (origin.x+distance, origin.y+distance)]


    @staticmethod
    def get_angle(origin, endpoint):
        dx = endpoint.x - origin.x
        dy = endpoint.y - origin.y
        return math.degrees(math.atan2(dy, dx))

    @staticmethod
    def get_distance(origin, endpoint):
        dx = endpoint.x - origin.x
        dy = endpoint.y - origin.y
        return math.floor(math.sqrt(math.pow(dx, 2) + math.pow(dy, 2)))



if __name__ == '__main__':
    path = '../GodRoss.jpg'
    bob = Fudged(path)
    bob.center_random(100)
    bob.save('../bobtest2.jpg')
