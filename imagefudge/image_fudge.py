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
        INPUTS:
            origins:   Iterable of tuples (x,y) OR Single tuple (x,y)
            endpoints: Iterable of tuples (x,y) OR Single tuple (x,y)
            arclen:    Iterable of length of at least 2 items containing
                       numeric values OR single numeric value
        OUTPUT:
            Edits Image object

        For each endpoint for every origin, gets the color at endpoint,
        computes the distance from origin to endpoint,
        and creates a bounding box that would encapsulate
        a circle of the radius described by distance.

        Next, the start and finish angles needed to create
        an arc of length arclen are computed.

        Finally the arc is drawn on the image.

        TODO:
            provide support for drawing arcs counter clockwise (- arclen)
            Draw arc on a separate layer.
            Give arc thickness.
        """
        if isinstance(endpoints, self.Point):
            endpoints = list(endpoints)
        if isinstance(origins, self.Point):
            origins = list(origins)

        for count, origin in enumerate(origins):
            print('Origin #: {}'.format(count))
            for endpoint in endpoints:
                color = self.image.getpixel(endpoint)
                distance = self.get_distance(origin, endpoint)
                bounding_box = self.make_bounding_box(origin, distance)
                angle = self.get_angle(origin, endpoint)
                try:
                    end_angle = angle + int(arclen)
                except (TypeError, ValueError):
                    try:
                        arclen_iter = arclen.__iter__()
                        end_angle = angle + randrange(int(next(arclen_iter)),
                                                      int(next(arclen_iter)))
                    except (TypeError,
                            ValueError,
                            AttributeError,
                            StopIteration) as e:
                        raise e(('arclen must be either a numeric '
                                 'value or subscriptable range'))
                finally:
                    ImageDraw.Draw(self.image).arc(bounding_box,
                                                   angle,
                                                   end_angle,
                                                   color)

class FudgeMaker(Fudged):
    """ """
    def fuzzy(self, magnitude):
        self.scale = 3
        point_number = int(magnitude)%10*10000
        origin_number = int(magnitude)%10*10+10
        print('Point Number: {}'.format(point_number))
        print('Origin Number: {}'.format(origin_number))
        random_endpoints = {x for x in self.random_points(point_number)}
        self.draw_relative_arcs(self.random_points(origin_number),
                                random_endpoints,
                                {1,2})

if __name__ == '__main__':

    img_path = 'htdocs/static/img/portland.jpg'
    save_path = 'htdocs/static/img/preview.jpg'
    fm = FudgeMaker(img_path)
    fm.fuzzy(9)
    fm.save(save_path)
