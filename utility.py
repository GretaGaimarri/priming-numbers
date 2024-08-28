import os
import pandas as pd
from psychopy import visual, core, event
import math
import random

def load_adjectives(filepath):
    """Load the adjectives from an Excel file and create congruent and incongruent datasets."""
    adjectives = pd.read_excel(filepath)
    adjectives_congruent = adjectives.copy()
    adjectives_congruent['congruent'] = 1

    adjectives_incongruent = adjectives.copy()
    adjectives_incongruent['congruent'] = 0

    return pd.concat([adjectives_congruent, adjectives_incongruent])

def create_window():
    """Create and return a PsychoPy visual window."""
    return visual.Window(fullscr=True, screen=0, allowGUI=True, allowStencil=False,
                         monitor='testMonitor', color=[0, 0, 0], colorSpace='rgb', blendMode='avg', useFBO=True)

def circles_overlap(x1, y1, x2, y2, radius):
    """
    Check if two circles overlap based on their center coordinates and radius.
    
    Parameters:
    x1, y1: float - Coordinates of the first circle's center.
    x2, y2: float - Coordinates of the second circle's center.
    radius: float - Radius of the circles.
    
    Returns:
    bool - True if the circles overlap, False otherwise.
    """
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance < 2 * radius

def find_valid_position(radius, existing_positions, x_bounds=(-0.5, 0.5), y_bounds=(-0.5, 0.5)):
    """
    Find a valid position for a circle that does not overlap with existing circles.
    
    Parameters:
    radius: float - Radius of the circle.
    existing_positions: list of tuples - List of existing circle positions as (x, y) tuples.
    x_bounds: tuple of floats - Minimum and maximum bounds for the x-coordinate.
    y_bounds: tuple of floats - Minimum and maximum bounds for the y-coordinate.
    
    Returns:
    tuple - (x, y) coordinates for a valid non-overlapping position.
    """
    while True:
        x = random.uniform(x_bounds[0] + radius, x_bounds[1] - radius)
        y = random.uniform(y_bounds[0] + radius, y_bounds[1] - radius)
        if all(not circles_overlap(x, y, px, py, radius) for px, py in existing_positions):
            return x, y


