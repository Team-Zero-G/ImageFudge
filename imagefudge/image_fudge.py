import math
import ntpath
from collections import namedtuple
from random import random, randrange
from PIL import Image
from PIL import ImageDraw

import os
import sys

sys.path.append(os.path.abspath('.'))
from imagefudge.utils import FudgeUtils


class Fudged(FudgeUtils):
    """ API Class for Image Fudge """

    def draw_relative_arcs(self, origins, endpoints, arclen):
        """ Draws an arc of length arclen.

        For each endpoint, gets the color at endpoint,
        computes the distance from origin to endpoint,
        and creates a bounding box that would encapsulate
        a circle of the radius described by distance.

        Next, the start and finish angles needed to create
        an arc of length arclen are computed.

        Finally the arc is drawn on the image.

        TODO:
            Draw arc on a separate layer.
            Give arc thickness.
            provide support for true negative arclen
        """
        if isinstance(endpoints, self.Point):
            endpoints = list(endpoints)
        if isinstance(origins, self.Point):
            origins = list(origins)

        for count, origin in enumerate(origins):
            print('Origin #: '.format(count))
            for endpoint in endpoints:
                color = self.image.getpixel(endpoint)
                distance = self.get_distance(origin, endpoint)
                bounding_box = self.make_bounding_box(origin, distance)
                angle = self.get_angle(origin, endpoint)
                try:
                    end_angle = angle + int(arclen)
                except (TypeError, ValueError):
                    try:
                        r_iter = arclen.__iter__().__next__
                        end_angle = angle + randrange(int(r_iter()),
                                                      int(r_iter()))
                    except (TypeError,
                            ValueError,
                            AttributeError,
                            StopIteration) as te:
                        raise TypeError(('arclen must be either a numeric '
                                         'value or subscriptable range'))
                finally:
                    ImageDraw.Draw(self.image).arc(bounding_box,
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


if __name__ == '__main__':

    img_path = 'htdocs/static/img/maxresdefault.jpg'
    save_path = 'htdocs/static/img/preview.jpg'
    bob = Fudged(img_path, scale=3)
    random_endpoints = [x for x in bob.random_points(10000)]
    bob.draw_relative_arcs(bob.random_points(100), random_endpoints, {1,2})
    bob.save(save_path)
