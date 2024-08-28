

from PIL import Image, ImageDraw
import random
import math
from utility import circles_overlap, find_valid_position

# image dimension
width, height = 700, 700 

# grey image
image = Image.new('RGB', (width, height), color=(128, 128, 128))

# print inside the image
draw = ImageDraw.Draw(image)

# print circles
def draw_circle(draw, x, y, radius, color):
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)



# define number of circles and radius
num_white_circles = 30
num_black_circles = 20
radius = 20

positions = []

        

# white circles
for _ in range(num_white_circles):
    x, y = find_valid_position(radius, positions, x_bounds=(radius, width-radius), y_bounds=(radius, height-radius))
    draw_circle(draw, x, y, radius, color=(255, 255, 255))
    positions.append((x, y))

# black circles
for _ in range(num_black_circles):
    x, y = find_valid_position(radius, positions, x_bounds=(radius, width-radius), y_bounds=(radius, height-radius))
    draw_circle(draw, x, y, radius, color=(0, 0, 0))
    positions.append((x, y))

# show the image
image.show()

