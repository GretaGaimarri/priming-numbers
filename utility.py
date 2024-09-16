import os
import pandas as pd
from psychopy import visual, core, event  # LP: some unused imports here
import math
import random

def get_next_participant_id(data_file_path):
    """
    Determines the next participant ID based on the existing data or sets it to 1 if no data exists.
    
    Args:
        data_file_path (str): The file path to the data CSV file.
        
    Returns:
        int: The next participant ID.
    """
    if os.path.exists(data_file_path):
        existing_data = pd.read_csv(data_file_path)
        if 'participant_id' in existing_data.columns:
            last_participant_id = existing_data['participant_id'].max()
            return last_participant_id + 1
        else:
            return 1
    else:
        return 1
    

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

def get_general_instructions(win):
    """ Define general instructions for the experiments"""
    return visual.TextStim(win=win, name='general_instructions', 
                               text="Grazie per aver scelto di partecipare all'esperimento. \n\nIl compito è diviso in due parti tra le quali ci sarà una breve pausa. \n\nQuando sei pronto/a premi un tasto qualsiasi per leggere le istruzioni.",
                               font='Arial', pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0,
                               color='white', colorSpace='rgb', opacity=1, languageStyle='LTR', depth=0.0)

def get_pause(win):
    """ Define the pause """
    return visual.TextStim(win=win, name='pause_text',
                             text="Fine prima parte. Puoi fare una breve pausa. Quando sei pronto/a per continuare, premi un tasto qualsiasi.",
                             font='Arial', pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0,
                             color='white', colorSpace='rgb', opacity=1, languageStyle='LTR', depth=0.0)
    
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


