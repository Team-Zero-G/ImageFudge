import math
from random import random
from PIL import Image
from PIL import ImageDraw

from collections import namedtuple


path = '../GodRoss.jpg'
bob = Image.open(path)

Point = namedtuple('Point', ['x', 'y'])
Dimention = namedtuple('Dimention', ['width', 'height'])

dimention = Dimention(width=bob.size[0], height=bob.size[1])

center_point = Point(x=dimention.width/2, y=dimention.height/2)

def draw_relative_arc(origin, endpoint, image):
    color = image.getpixel(endpoint)
    angle = get_angle(origin, endpoint)
    distance = get_distance(origin, endpoint)
    bounding_box = make_bounding_box(origin, distance)
    arc = int(random()*360)
    while arc == angle:
        arc = int(random()*360)

    draw = ImageDraw.Draw(image).arc(bounding_box, angle, arc, color)


def make_bounding_box(origin, distance):
    return [(origin.x-distance, origin.y-distance),
            (origin.x+distance, origin.y+distance)]

def select_point(dimention):
    return Point(int(random()*dimention.width), int(random()*dimention.height))

def get_angle(origin, endpoint):
    dx = endpoint.x - origin.x
    dy = endpoint.y - origin.y
    return math.degrees(math.atan2(dy, dx))

def get_distance(origin, endpoint):
    dx = endpoint.x - origin.x
    dy = endpoint.y - origin.y
    return math.floor(math.sqrt(math.pow(dx, 2) + math.pow(dy, 2)))

#draw = ImageDraw.Draw(bob).arc([(20, 100),(120, 200)], 180, 270, "#333333")
for i in range(100):
    draw_relative_arc(center_point, select_point(dimention), bob)

bob.save('../bobtest.jpg')
print(bob.size)
