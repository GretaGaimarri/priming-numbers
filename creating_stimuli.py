

from PIL import Image, ImageDraw
import random
import math

# image dimension
width, height = 700, 700 

# grey image
image = Image.new('RGB', (width, height), color=(128, 128, 128))

# print inside the image
draw = ImageDraw.Draw(image)

# print circles
def draw_circle(draw, x, y, radius, color):
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)

# not overlapping circles
def circles_overlap(x1, y1, x2, y2, radius):
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance < 2 * radius


# define number of circles and radius
num_white_circles = 30
num_black_circles = 20
radius = 20

positions = []


# find the right position for each circle
def find_valid_position(radius):
    while True:
        x = random.randint(radius, width - radius)
        y = random.randint(radius, height - radius)
        if all(not circles_overlap(x, y, px, py, radius) for px, py in positions):
            return x, y
        
# white circles
for _ in range(num_white_circles):
    x, y = find_valid_position(radius)
    draw_circle(draw, x, y, radius, color=(255, 255, 255))
    positions.append((x, y))

# black circles
for _ in range(num_black_circles):
    x, y = find_valid_position(radius)
    draw_circle(draw, x, y, radius, color=(0, 0, 0))
    positions.append((x, y))

# show the image
image.show()

