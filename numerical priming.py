
from psychopy import visual, core, event, logging, data
import pandas as pd
import random
from utility import load_adjectives, create_window, get_general_instructions, get_next_participant_id, get_pause


# Determine participant ID based on previous data or set it to 1
data_file_path = 'data.csv'

participant_id = get_next_participant_id(data_file_path)

# Load adjectives
adjectives_combined = load_adjectives(r"C:\Users\greta\my_project\adjectives.xlsx")
print(adjectives_combined)

# Window settings in utility
win = create_window()

# Instructions, Puase, Fixation cross, prime and target
general_instructions = get_general_instructions(win)
# Specific Instructions for two runs (in the second one response buttons are reversed to avoid any possible influence on results)
instructions_run_one = visual.TextStim(win=win, name='instructions_run_one', 
                               text="Ecco le istruzioni: \n\n Sullo schermo appariranno dei numeri da 1 a 9. \n\nPremi 't' se pensi che il numero sia minore di 5.\n"
                                    "Premi 'v' se pensi che il numero sia maggiore di 5.\n\n"
                                    "Ricorda che sei libero/a di abbandonare l'esperimento in qualsiasi momento, premendo il tasto 'escape'.\n\n"
                                    "Premi un tasto qualsiasi per iniziare.",
                               font='Arial', pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0,
                               color='white', colorSpace='rgb', opacity=1, languageStyle='LTR', depth=0.0)

instructions_run_two = visual.TextStim(win=win, name='instructions_run_two', 
                               text="Sullo schermo appariranno dei numeri da 1 a 9. \n\nPremi 'v' se pensi che il numero sia minore di 5.\n"
                                    "Premi 't' se pensi che il numero sia maggiore di 5.\n\n"
                                    "Ricorda che sei libero/a di abbandonare l'esperimento in qualsiasi momento, premendo il tasto 'escape'.\n\n"
                                    "Premi un tasto qualsiasi per iniziare.",
                               font='Arial', pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0,
                               color='white', colorSpace='rgb', opacity=1, languageStyle='LTR', depth=0.0)

pause_text = get_pause(win)

fixation = visual.TextStim(win=win, name='fixation', text='+', font='Arial', pos=(0, 0), height=0.2, wrapWidth=None, ori=0,
                           color='white', colorSpace='rgb', opacity=1, languageStyle='LTR', depth=0.0)
prime = visual.TextStim(win=win, name='prime', text='', font='Arial', pos=(0, 0), height=0.2, wrapWidth=None, ori=0,
                        color='white', colorSpace='rgb', opacity=1, languageStyle='LTR', depth=0.0)
number_stim = visual.TextStim(win=win, name='number', text='', font='Arial', pos=(0, 0), height=0.2, wrapWidth=None, ori=0,
                              color='white', colorSpace='rgb', opacity=1, languageStyle='LTR', depth=0.0)


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


def run_trial(prime_text, bigsmall_value, congruent, reverse=False):
    # Check for escape key
    if 'escape' in event.getKeys():
        core.quit()

    # Fixation cross
    fixation.draw()
    win.flip()
    core.wait(1.0)  # 1000 ms

    # Prime display
    prime.setText(prime_text)
    prime.draw()
    win.flip()
    core.wait(0.043)  # 43 ms

    # Check for escape key
    if 'escape' in event.getKeys():
        core.quit()

    # Target presentation
    if congruent:
        if bigsmall_value == 1:
            number = random.choice([6, 7, 8, 9]) 
        else:
            number = random.choice([1, 2, 3, 4])  
    else:
        if bigsmall_value == 1:
            number = random.choice([1, 2, 3, 4])  
        else:
            number = random.choice([6, 7, 8, 9])  

    number_stim.setText(str(number))
    number_stim.draw()
    win.flip()

    # Reset the clock to 0 when the target appears
    rt_clock = core.Clock()
    rt_clock.reset()

    # Record the response and reaction times
    response = event.waitKeys(keyList=['t', 'v', 'escape'])
    if 'escape' in response:
        core.quit()
    reaction_time = rt_clock.getTime()  # Get the time since the target appeared

    # Determine accuracy
    if reverse:
        if (congruent and ((bigsmall_value == 1 and response[0] == 'v') or (bigsmall_value == 0 and response[0] == 't'))) or \
           (not congruent and ((bigsmall_value == 1 and response[0] == 't') or (bigsmall_value == 0 and response[0] == 'v'))):
            accuracy = '1'
        else:
            accuracy = '0'
    else:
        if (congruent and ((bigsmall_value == 1 and response[0] == 't') or (bigsmall_value == 0 and response[0] == 'v'))) or \
           (not congruent and ((bigsmall_value == 1 and response[0] == 'v') or (bigsmall_value == 0 and response[0] == 't'))):
            accuracy = '1'
        else:
            accuracy = '0'

    return response, reaction_time, accuracy

def run_first():
    run_instructions(instructions_run_one)
    # Run the first set of trials
    for trial in trial_sequence:
        prime_text = trial['word']
        big_small_value = trial['bigsmall']
        dimension = trial['dimension'] 
        congruent = trial['congruent'] == 1
        response, reaction_time, accuracy = run_trial(prime_text, big_small_value, congruent)
        trial_data.append((participant_id, prime_text, big_small_value, dimension, congruent, response[0], reaction_time, accuracy, 'first_run'))

def run_second():
    run_instructions(instructions_run_two)
    # Run the second set of trials with reversed keys
    trial_sequence_second_run = data.TrialHandler(nReps=1, method='random', trialList=adjectives_combined.to_dict('records'), seed=None, name='trials_second_run')
    
    for trial in trial_sequence_second_run:
        prime_text = trial['word']
        big_small_value = trial['bigsmall']
        dimension = trial['dimension'] 
        congruent = trial['congruent'] == 1
        response, reaction_time, accuracy = run_trial(prime_text, big_small_value, congruent, reverse=True) #reverse true to invert the accuracy method 
        trial_data.append((participant_id, prime_text, big_small_value, dimension, congruent, response[0], reaction_time, accuracy, 'second_run'))

# Run the experiment
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



with open('data.csv', 'w') as data_file:
    data_file.write('prime,big_small,congruent,response,reaction_time,accuracy,number,run\n')
    for data_point in trial_data:
        data_file.write(f"{data_point[0]},{data_point[1]},{data_point[2]},{data_point[3]},{data_point[4]:.4f},{data_point[5]},{data_point[6]},{data_point[7]}\n")

win.close()
core.quit()

  

   
   
