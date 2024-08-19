import pandas as pd
from psychopy import visual, core, event, logging, data
import random

# Load adjectives
adjectives = pd.read_excel(r'C:djectives.xlsx')

# Create duplicated trials for each word-opposite pair with color variations
adjectives_white_word = adjectives.copy()
adjectives_white_word['prime_color'] = 'white'
adjectives_white_word['opposite_color'] = 'black'

adjectives_black_word = adjectives.copy()
adjectives_black_word['prime_color'] = 'black'
adjectives_black_word['opposite_color'] = 'white'

# Combine into one DataFrame
adjectives_combined = pd.concat([adjectives_white_word, adjectives_black_word])

# Add congruent/incongruent flag (assuming you want both versions)
adjectives_congruent = adjectives_combined.copy()
adjectives_congruent['congruent'] = 1

adjectives_incongruent = adjectives_combined.copy()
adjectives_incongruent['congruent'] = 0

adjectives_combined = pd.concat([adjectives_congruent, adjectives_incongruent])

# Ensure that 'congruent' column is present
print(adjectives_combined.head())  # Print the first few rows to verify

# Window settings
win = visual.Window(fullscr=True, screen=0, allowGUI=True, allowStencil=False,
                    monitor='testMonitor', color=[0, 0, 0], colorSpace='rgb', blendMode='avg', useFBO=True)

# Instructions, Pause, Fixation cross, prime and target
instructions = visual.TextStim(win=win, name='instructions', 
                               text="Benvenuto/a all'esperimento.\n\nPremi 't' se pensi che il gruppo di punti più numeroso sia bianco.\n"
                                    "Premi 'v' se pensi che il gruppo di punti più numeroso sia nero.\n\n"
                                    "Sei libero/a di abbandonare l'esperimento in qualsiasi momento, prememndo il tasto 'escape'.\n\n"
                                    "Premi un tasto per iniziare.",
                               font='Arial', pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0,
                               color='white', colorSpace='rgb', opacity=1, languageStyle='LTR', depth=0.0)
pause_text = visual.TextStim(win=win, name='pause_text',
                             text="Fine prima parte.\n\n" "Premi un qualsiasi pulsante per iniziare la seconda parte dell'esperimento.",
                             font='Arial', pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0,
                             color='white', colorSpace='rgb', opacity=1, languageStyle='LTR', depth=0.0)
fixation = visual.TextStim(win=win, name='fixation', text='+', font='Arial', pos=(0, 0), height=0.2, wrapWidth=None, ori=0,
                           color='white', colorSpace='rgb', opacity=1, languageStyle='LTR', depth=0.0)

# Two adjectives display
prime_top = visual.TextStim(win=win, name='prime_top', text='', font='Arial', pos=(0, 0.1), height=0.2, wrapWidth=None, ori=0,
                            color='white', colorSpace='rgb', opacity=1, languageStyle='LTR', depth=0.0)
prime_bottom = visual.TextStim(win=win, name='prime_bottom', text='', font='Arial', pos=(0, -0.1), height=0.2, wrapWidth=None, ori=0,
                               color='black', colorSpace='rgb', opacity=1, languageStyle='LTR', depth=0.0)

# Create trial sequence
trial_sequence = data.TrialHandler(nReps=1, method='random', trialList=adjectives_combined.to_dict('records'), seed=None, name='trials')

def run_instructions():
    instructions.draw()
    win.flip()
    keys = event.waitKeys() 
    if 'escape' in keys:
        core.quit()

def run_pause():
    pause_text.draw()
    win.flip()
    keys = event.waitKeys()  
    if 'escape' in keys:
        core.quit()

def run_trial(prime_text, opposite_text, prime_color, opposite_color, bigsmall_value, congruent, reverse=False):
    # Check for escape key
    if 'escape' in event.getKeys():
        core.quit()

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

    # Check for escape key
    if 'escape' in event.getKeys():
        core.quit()

    # Create two groups of dots
    num_dots_black = random.randint(5, 15)
    num_dots_white = random.randint(5, 15)

    # Determine which color should have the larger/smaller number of dots based on congruence and bigsmall
    if congruent:
        if bigsmall_value == 1:
            # The group of dots matching the prime color should have more dots
            if prime_color == 'black' and num_dots_black < num_dots_white:
                num_dots_black, num_dots_white = num_dots_white, num_dots_black
            elif prime_color == 'white' and num_dots_white < num_dots_black:
                num_dots_black, num_dots_white = num_dots_white, num_dots_black
        elif bigsmall_value == 0:
            # The group of dots matching the prime color should have fewer dots
            if prime_color == 'black' and num_dots_black > num_dots_white:
                num_dots_black, num_dots_white = num_dots_white, num_dots_black
            elif prime_color == 'white' and num_dots_white > num_dots_black:
                num_dots_black, num_dots_white = num_dots_white, num_dots_black
    else:  # Incongruent condition
        if bigsmall_value == 1:
            # The group of dots matching the prime color should have fewer dots
            if prime_color == 'black' and num_dots_black > num_dots_white:
                num_dots_black, num_dots_white = num_dots_white, num_dots_black
            elif prime_color == 'white' and num_dots_white > num_dots_black:
                num_dots_black, num_dots_white = num_dots_white, num_dots_black
        elif bigsmall_value == 0:
            # The group of dots matching the prime color should have more dots
            if prime_color == 'black' and num_dots_black < num_dots_white:
                num_dots_black, num_dots_white = num_dots_white, num_dots_black
            elif prime_color == 'white' and num_dots_white < num_dots_black:
                num_dots_black, num_dots_white = num_dots_white, num_dots_black

    # Recreate the ElementArrayStim after adjusting the number of elements
    dots_black = visual.ElementArrayStim(
        win=win,
        nElements=num_dots_black,
        elementTex=None,
        elementMask='circle',
        xys=[(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)) for _ in range(num_dots_black)],
        sizes=0.05,
        colors='black'
    )
    
    dots_white = visual.ElementArrayStim(
        win=win,
        nElements=num_dots_white,
        elementTex=None,
        elementMask='circle',
        xys=[(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)) for _ in range(num_dots_white)],
        sizes=0.05,
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

    # Determine accuracy
    correct_response = 't' if num_dots_white > num_dots_black else 'v'
    accuracy = '1' if response[0] == correct_response else '0'

    return response, reaction_time, accuracy


# Run the experiment
logging.console.setLevel(logging.WARNING)
trial_data = []

# First run instructions and trials
run_instructions()  

for trial in trial_sequence:
    prime_text = trial['word']
    opposite_text = trial['opposite']
    prime_color = trial['prime_color']
    opposite_color = trial['opposite_color']
    big_small_value = trial['bigsmall']
    congruent = trial['congruent'] == 1
    response, reaction_time, accuracy = run_trial(prime_text, opposite_text, prime_color, opposite_color, big_small_value, congruent)
    trial_data.append((prime_text, opposite_text, prime_color, opposite_color, big_small_value, congruent, response[0], reaction_time, accuracy, 'first_run'))

# Pause before the second part
run_pause()

# Second run instructions and trials (reversed keys)
instructions.setText("Benvenuto/a alla seconda parte dell'esperimento.\n\nPremi 't' se pensi che il gruppo di punti più numeroso sia bianco.\n"
                     "Premi 'v' se pensi che il gruppo di punti più numeroso sia nero.\n\n"
                     "Sei libero/a di abbandonare l'esperimento in qualsiasi momento, prememndo il tasto 'escape'.\n\n"
                     "Premi un tasto per iniziare.")
run_instructions()  

trial_sequence_second_run = data.TrialHandler(nReps=1, method='random', trialList=adjectives_combined.to_dict('records'), seed=None, name='trials_second_run')

for trial in trial_sequence_second_run:
    prime_text = trial['word']
    opposite_text = trial['opposite']
    prime_color = trial['prime_color']
    opposite_color = trial['opposite_color']
    big_small_value = trial['bigsmall']
    congruent = trial['congruent'] == 1
    response, reaction_time, accuracy = run_trial(prime_text, opposite_text, prime_color, opposite_color, big_small_value, congruent, reverse=True)
    trial_data.append((prime_text, opposite_text, prime_color, opposite_color, big_small_value, congruent, response[0], reaction_time, accuracy, 'second_run'))

with open('data.csv', 'w') as data_file:
    data_file.write('prime,opposite,prime_color,opposite_color,big_small,congruent,response,reaction_time,accuracy,run\n')
    for data_point in trial_data:
        data_file.write(f"{data_point[0]},{data_point[1]},{data_point[2]},{data_point[3]},{data_point[4]},{data_point[5]},{data_point[6]},{data_point[7]:.4f},{data_point[8]}\n")

win.close()
core.quit()

