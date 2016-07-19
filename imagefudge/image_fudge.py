import math
import ntpath
import os
from random import random, randrange
from PIL import Image
from PIL import ImageDraw

from collections import namedtuple
from imagefudge.utils import FudgeUtils


class Fudged(FudgeUtils):
    """ API Class for Image Fudge """

    def draw_relative_arcs(self, origin, endpoints, arclen):
        """ Draws an arc of length arclen.

        For each endpoint, gets the color at endpoint,
        computes the distance from origin to endpoint,
        and creates a bounding box that would encapsulate
        a circle of the radius described by distance.

        Next, the start and finish angles needed to create
        an arc of length arclen are computed.

        Finally the arc is drawn on the image.
        """

        if isinstance(endpoints, self.Point):
            endpoints = [endpoints]
        for endpoint in endpoints:
            color = self.image.getpixel(endpoint)
            distance = self.get_distance(origin, endpoint)
            bounding_box = self.make_bounding_box(origin, distance)
            angle = self.get_angle(origin, endpoint)
            try:
                if arclen > 360 and arclen < -360:
                    raise ValueError('arclen must be between -360 and 360')
            except TypeError as te:
                try:
                    if arclen[0] > 360 and arclen < -360 or\
                       arclen[1] > 360 and arclen < -360:
                        raise ValueError('arclen must be between -360 and 360')
                    arclen = randrange(arclen[0], arclen[1])
                except IndexError: raise te(('arclen must be either a numeric'
                                             'value or subscriptable range'))

            end_angle = angle + arclen
            # TODO: Draw arc on a separate layer.
            # TODO: Give arc thickness.
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


def test_multi_origin(path, test_num):

    bob = Fudged(path)
    bob.draw_arcs_multi_origin(100, 1000, (10, 20))
    bob.save('htdocs/static/img/preview.jpg')


if __name__ == '__main__':

    path = 'htdocs/static/img/mt_hood_original.jpg'
    test_multi_origin(path, 4)
