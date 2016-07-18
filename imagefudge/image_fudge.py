import math
import ntpath
import os
from random import random, randrange
from PIL import Image
from PIL import ImageDraw

from collections import namedtuple
from imagefudge.utils import FudgeUtils


class Fudged(FudgeUtils):
    """ """

    def draw_relative_arcs(self, origin, endpoints, arclen):

        if isinstance(endpoints, self.Point):
            endpoints = [endpoints]
        for endpoint in endpoints:
            color = self.image.getpixel(endpoint)
            distance = self.get_distance(origin, endpoint)
            bounding_box = self.make_bounding_box(origin, distance)
            angle = self.get_angle(origin, endpoint)
            try:
                if arclen > 360 and arclen < -360: raise ValueError
            except TypeError as e:
                try:
                    if arclen[0] > 360 and arclen < -360: raise ValueError
                    if arclen[1] > 360 and arclen < -360: raise ValueError
                    arclen = randrange(arclen[0], arclen[1])
                except IndexError: raise e

            end_angle = angle + arclen
            draw = ImageDraw.Draw(self.image).arc(bounding_box,
                                                  angle,
                                                  end_angle,
                                                  color)


    def draw_arcs_custom_origin(self, point_number, arc_len, origin):

        self.draw_relative_arcs(origin,
                                self.random_points(point_number),
                                arc_len)

    def draw_arcs_center_origin(self, point_number, arc_len):

        self.draw_relative_arcs(self.get_center(),
                                self.random_points(point_number),
                                arc_len)

    def draw_arcs_multi_origin(self, origin_number, point_number, arc_len):

        for origin in self.random_points(origin_number):
            self.draw_relative_arcs(origin,
                                    self.random_points(point_number),
                                    arc_len)

    #def calculate_relative_point(self, relative_point):


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


def test_multi_origin(path, test_num):

    #for i in range(test_num):
    bob = Fudged(path)
    bob.draw_arcs_multi_origin(100, 1000, (10, 20))
    #bob.draw_arcs_custom_origin(1000, (10, 30), bob.Point(bob.get_center()[0], bob.height//3))
    bob.save('htdocs/static/img/preview.jpg')


if __name__ == '__main__':

    path = 'htdocs/static/img/mt_hood_original.jpg'
    test_multi_origin(path, 4)

    #test_many_random(path, 5, 3)
