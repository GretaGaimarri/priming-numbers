
import os
import random
import psychopy
from psychopy import visual, core, event, logging, data
import pandas as pd
import math
from utility import find_valid_position, create_window



# Determine participant ID based on previous data or set it to 1
data_file_path = 'data_dots.csv'

if os.path.exists(data_file_path):
    existing_data = pd.read_csv(data_file_path)
    if 'participant_id' in existing_data.columns:
        last_participant_id = existing_data['participant_id'].max()
        participant_id = last_participant_id + 1
    else:
        participant_id = 1
else:
    participant_id = 1

# Load adjectives file and print it
adjectives = pd.read_excel(r"C:\Users\greta\my_project\adjectives.xlsx")
print(adjectives)


# Create duplicated trials for each word-opposite pair with color variations (black and white)
adjectives_white_word = adjectives.copy()
adjectives_white_word['prime_color'] = 'white'
adjectives_white_word['opposite_color'] = 'black'


adjectives_black_word = adjectives.copy()
adjectives_black_word['prime_color'] = 'black'
adjectives_black_word['opposite_color'] = 'white'


# Combine into one dataframe
adjectives_combined = pd.concat([adjectives_white_word, adjectives_black_word])
print(adjectives_combined)

# Add congruent/incongruent flag 
adjectives_congruent = adjectives_combined.copy()
adjectives_congruent['congruent'] = 1

adjectives_incongruent = adjectives_combined.copy()
adjectives_incongruent['congruent'] = 0

adjectives_combined = pd.concat([adjectives_congruent, adjectives_incongruent])

# Window settings in utility
win = create_window()

# General Instructions
general_instructions = visual.TextStim(win=win, name='general_instructions', 
                               text="Grazie per aver scelto di partecipare all'esperimento. \n\nIl compito è diviso in due parti tra le quali ci sarà una breve pausa. \n\nQuando sei pronto/a premi un tasto qualsiasi per leggere le istruzioni.",
                               font='Arial', pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0,
                               color='white', colorSpace='rgb', opacity=1, languageStyle='LTR', depth=0.0)

# Specific Instructions for two runs (in the second one response buttons are reversed to avoid any possible influence on results)
instructions_run_one = visual.TextStim(win=win, name='instructions_run_one', 
                               text="Ecco le istruzioni: \n\nDue gruppi di pallini (neri e bianchi) appariranno sullo schermo. \n\nPremi 't' se pensi che il gruppo di punti più numeroso sia bianco.\n"
                                    "Premi 'v' se pensi che il gruppo di punti più numeroso sia nero.\n\n"
                                    "Ricorda che sei libero/a di abbandonare l'esperimento in qualsiasi momento, premendo il tasto 'escape'.\n\n"
                                    "Premi un tasto per iniziare.",
                               font='Arial', pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0,
                               color='white', colorSpace='rgb', opacity=1, languageStyle='LTR', depth=0.0)

instructions_run_two = visual.TextStim(win=win, name='instructions_run_two', 
                               text="Due gruppi di pallini (neri e bianchi) appariranno sullo schermo. \n\nPremi 't' se pensi che il gruppo di punti più numeroso sia bianco.\n"
                                    "Premi 'v' se pensi che il gruppo di punti più numeroso sia nero.\n\n"
                                    "Ricorda che sei libero/a di abbandonare l'esperimento in qualsiasi momento, premendo il tasto 'escape'.\n\n"
                                    "Premi un tasto per iniziare.",
                               font='Arial', pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0,
                               color='white', colorSpace='rgb', opacity=1, languageStyle='LTR', depth=0.0)

pause_text = visual.TextStim(win=win, name='pause_text',
                             text="Fine prima parte. Puoi fare una breve pausa. Quando sei pronto/a per continuare, premi un tasto qualsiasi.",
                             font='Arial', pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0,
                             color='white', colorSpace='rgb', opacity=1, languageStyle='LTR', depth=0.0)

# Fixation cross
fixation = visual.TextStim(win=win, name='fixation', text='+', font='Arial', pos=(0, 0), height=0.2, wrapWidth=None, ori=0,
                           color='white', colorSpace='rgb', opacity=1, languageStyle='LTR', depth=0.0)

# Two adjectives display
prime_top = visual.TextStim(win=win, name='prime_top', text='', font='Arial', pos=(0, 0.1), height=0.2, wrapWidth=None, ori=0,
                            color='white', colorSpace='rgb', opacity=1, languageStyle='LTR', depth=0.0)
prime_bottom = visual.TextStim(win=win, name='prime_bottom', text='', font='Arial', pos=(0, -0.1), height=0.2, wrapWidth=None, ori=0,
                               color='black', colorSpace='rgb', opacity=1, languageStyle='LTR', depth=0.0)

# Create trial sequence
trial_sequence = data.TrialHandler(nReps=1, method='random', trialList=adjectives_combined.to_dict('records'), seed=None, name='trials')

def show_general_instructions():
    general_instructions.draw()
    win.flip()
    keys = event.waitKeys()
    if 'escape' in keys:
        core.quit()

def run_instructions(instructions):
    instructions.draw()
    win.flip()
    keys = event.waitKeys() 
    if 'escape' in keys:
        core.quit()

def show_pause():
    pause_text.draw()
    win.flip()
    keys = event.waitKeys()
    if 'escape' in keys:
        core.quit()

def run_trial(prime_text, opposite_text, prime_color, opposite_color, bigsmall_value, congruent, reverse=False):
    # Fixation cross
    fixation.draw()
    win.flip()
    core.wait(1.0)  # 1000 ms

    # Set colors and texts
    prime_top.setText(prime_text)
    prime_top.setColor(prime_color)
    prime_bottom.setText(opposite_text)
    prime_bottom.setColor(opposite_color)

    # Display primes
    prime_top.draw()
    prime_bottom.draw()
    win.flip()
    core.wait(0.043)  # 43 ms

    circle_radius = 0.05

    # Create two groups of dots
    num_dots_black = random.randint(5, 15)
    num_dots_white = random.randint(5, 15)

        # Adjust number of dots based on congruence and bigsmall value
    if congruent:
        if bigsmall_value == 1:
            if prime_color == 'black' and num_dots_black < num_dots_white:
                num_dots_black, num_dots_white = num_dots_white, num_dots_black
            elif prime_color == 'white' and num_dots_white < num_dots_black:
                num_dots_black, num_dots_white = num_dots_white, num_dots_black
        elif bigsmall_value == 0:
            if prime_color == 'black' and num_dots_black > num_dots_white:
                num_dots_black, num_dots_white = num_dots_white, num_dots_black
            elif prime_color == 'white' and num_dots_white > num_dots_black:
                num_dots_black, num_dots_white = num_dots_white, num_dots_black
    else:
        if bigsmall_value == 1:
            if prime_color == 'black' and num_dots_black > num_dots_white:
                num_dots_black, num_dots_white = num_dots_white, num_dots_black
            elif prime_color == 'white' and num_dots_white > num_dots_black:
                num_dots_black, num_dots_white = num_dots_white, num_dots_black
        elif bigsmall_value == 0:
            if prime_color == 'black' and num_dots_black < num_dots_white:
                num_dots_black, num_dots_white = num_dots_white, num_dots_black
            elif prime_color == 'white' and num_dots_white < num_dots_black:
                num_dots_black, num_dots_white = num_dots_white, num_dots_black


    positions_black = []
    for _ in range(num_dots_black):
        x, y = find_valid_position(circle_radius, positions_black)
        positions_black.append((x, y))

    dots_black = visual.ElementArrayStim(
        win=win,
        nElements=num_dots_black,
        elementTex=None,
        elementMask='circle',
        xys=positions_black,
        sizes=circle_radius * 2, 
        colors='black'
    )

    
    positions_white = []
    for _ in range(num_dots_white):
        x, y = find_valid_position(circle_radius, positions_black + positions_white)  
        positions_white.append((x, y))

    dots_white = visual.ElementArrayStim(
        win=win,
        nElements=num_dots_white,
        elementTex=None,
        elementMask='circle',
        xys=positions_white,
        sizes=circle_radius * 2,  
        colors='white'
    )


    # Display the dots
    dots_black.draw()
    dots_white.draw()
    win.flip()

    # Reset the clock to 0 when the dots appear
    rt_clock = core.Clock()
    rt_clock.reset()

    # Record the response and reaction times
    response = event.waitKeys(keyList=['t', 'v', 'escape'])
    if 'escape' in response:
        core.quit()
    reaction_time = rt_clock.getTime()  # Get the time since the dots appeared

    # Determine accuracy based on the `reverse` parameter
    if reverse:
        correct_response = 'v' if num_dots_white > num_dots_black else 't'
    else:
        correct_response = 't' if num_dots_white > num_dots_black else 'v'

    accuracy = '1' if response[0] == correct_response else '0'

    return response, reaction_time, accuracy

def run_first():
    run_instructions(instructions_run_one)
    # Run the first set of trials
    for trial in trial_sequence:
        prime_text = trial['word']
        opposite_text = trial['opposite']
        prime_color = trial['prime_color']
        opposite_color = trial['opposite_color']
        big_small_value = trial['bigsmall']
        dimension = trial['dimension'] 
        congruent = trial['congruent'] == 1
        response, reaction_time, accuracy = run_trial(prime_text, opposite_text, prime_color, opposite_color, big_small_value, congruent)
        trial_data.append((participant_id, prime_text, opposite_text, prime_color, opposite_color, big_small_value, dimension, congruent, response[0], reaction_time, accuracy, 'first_run'))

def run_second():
    run_instructions(instructions_run_two)
    # Run the second set of trials with reversed keys
    trial_sequence_second_run = data.TrialHandler(nReps=1, method='random', trialList=adjectives_combined.to_dict('records'), seed=None, name='trials_second_run')
    
    for trial in trial_sequence_second_run:
        prime_text = trial['word']
        opposite_text = trial['opposite']
        prime_color = trial['prime_color']
        opposite_color = trial['opposite_color']
        big_small_value = trial['bigsmall']
        dimension = trial['dimension'] 
        congruent = trial['congruent'] == 1
        response, reaction_time, accuracy = run_trial(prime_text, opposite_text, prime_color, opposite_color, big_small_value, congruent, reverse=True) #reverse true to invert the accuracy method 
        trial_data.append((participant_id, prime_text, opposite_text, prime_color, opposite_color, big_small_value, dimension, congruent, response[0], reaction_time, accuracy, 'second_run'))

# Run the experiment with counterbalanced order
logging.console.setLevel(logging.WARNING)
trial_data = []

# Show general instructions first
show_general_instructions()

# Randomly choose which run to present first
if random.choice([True, False]):
    run_first()
    show_pause()
    run_second()
else:
    run_second()
    show_pause()
    run_first()

# Save the data
with open('data_dots.csv', 'a') as data_file:
    for data_point in trial_data:
        data_file.write(f"{data_point[0]},{data_point[1]},{data_point[2]},{data_point[3]},{data_point[4]},{data_point[5]},{data_point[6]},{data_point[7]:.4f},{data_point[8]}\n")

win.close()
core.quit()
  
