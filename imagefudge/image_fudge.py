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
            arclen:    1) static numeric value (or iterable of len 1)
                       2) Iterable vector (x,y) of for random range between x,y
                       3) Iterable with more than 2 items

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
        print(self.image.size)

        # Attempt to create arclen_itter if arclen itterable is greater than 3
        try:
            tmp_arclen_iter = arclen.__iter__()
            count_holder = -1
            for count, _ in enumerate(tmp_arclen_iter):
                count_holder = count
                if count is 2:
                    arclen_iter = arclen.__iter__()
                    break
            if count_holder is 0: # If iter lenth 1 set arclen to iter value
                tmp_arclen_iter = arclen.__iter__()
                arclen = int(next(tmp_arclen_iter))

        except AttributeError:  # Pass if arclen is not iterable
            pass
        except ValueError as e:  # raise if 1st item of iter len 1 is not numeric
            raise e(('arclen must be either a numeric value,'
                     'subscriptable range, or iterable'))

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
                        end_angle = angle + int(next(arclen_iter))
                    except UnboundLocalError:
                        try:
                            arclen_iter = arclen.__iter__()
                            end_angle = angle + randrange(int(next(arclen_iter)),
                                                          int(next(arclen_iter)))
                        except (TypeError, ValueError) as e:
                            raise e(('arclen must be either a numeric value,'
                                     'subscriptable range, or iterable'))
                    except StopIteration:
                        arclen_iter = arclen.__iter__()
                        end_angle = angle + int(next(arclen_iter))
                    except (TypeError, ValueError) as e:
                        raise e(('arclen must be either a numeric '
                                 'value, subscriptable range, or iterable'))
                finally:
                    ImageDraw.Draw(self.image).arc(bounding_box,
                                                   angle,
                                                   end_angle,
                                                   color)

class FudgeMaker(Fudged):
    """ """
    @FudgeUtils.anti_alias(scale=5)
    def fuzzy(self, magnitude):
        point_number = int(magnitude) % 10*10000
        origin_number = int(magnitude) % 10*10+10
        print('Point Number: {}'.format(point_number))
        print('Origin Number: {}'.format(origin_number))
        random_endpoints = {x for x in self.random_points(point_number)}
        print(random_endpoints)
        self.draw_relative_arcs(self.random_points(origin_number),
                                random_endpoints, {1, 2})

    def test1(self):
        random_endpoints = {self.random_points(100) for x in range(100)}
        print(random_endpoints)
        self.draw_relative_arcs(self.random_points(100),
                                self.random_points(100),
                                range(20))


if __name__ == '__main__':

    img_path = 'htdocs/static/img/portland.jpg'
    save_path = 'htdocs/static/img/preview1.jpg'
    fm = FudgeMaker(img_path)
    #fm.fuzzy(3)
    fm.test1()
    fm.save(save_path)
