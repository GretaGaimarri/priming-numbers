from psychopy import visual, core, event, logging, data
import pandas as pd
import random

# Carica gli aggettivi dal file Excel
adjectives = pd.read_excel(r'C:\Users\greta\OneDrive\Desktop\pavlovia\adjectives.xlsx')
adjectives_congruent = adjectives.copy()
adjectives_congruent['congruent'] = 1

adjectives_incongruent = adjectives.copy()
adjectives_incongruent['congruent'] = 0

adjectives_combined = pd.concat([adjectives_congruent, adjectives_incongruent])

# Window fullscreen
win = visual.Window(fullscr=True, screen=0, allowGUI=True, allowStencil=False,
                    monitor='testMonitor', color=[0, 0, 0], colorSpace='rgb', blendMode='avg', useFBO=True)

# Instructions, fixation cross and stimuli
instructions = visual.TextStim(win=win, name='instructions', 
                               text="Benvenuto/a all'esperimento.\n\nPremi 't' se pensi che il numero sia maggiore di 5.\n"
                                    "Premi 'v' se pensi che il numero sia minore di 5.\n\n"
                                    "Sei libero/a di abbandonare l'esperimento in qualsiasi momento, prememndo il tasto 'escape'.\n\n"
                                    "Premi un tasto per iniziare.",
                               font='Arial', pos=(0, 0), height=0.08, wrapWidth=1.5, ori=0,
                               color='white', colorSpace='rgb', opacity=1, languageStyle='LTR', depth=0.0)
fixation = visual.TextStim(win=win, name='fixation', text='+', font='Arial', pos=(0, 0), height=0.2, wrapWidth=None, ori=0,
                           color='white', colorSpace='rgb', opacity=1, languageStyle='LTR', depth=0.0)
prime = visual.TextStim(win=win, name='prime', text='', font='Arial', pos=(0, 0), height=0.2, wrapWidth=None, ori=0,
                        color='white', colorSpace='rgb', opacity=1, languageStyle='LTR', depth=0.0)
number_stim = visual.TextStim(win=win, name='number', text='', font='Arial', pos=(0, 0), height=0.2, wrapWidth=None, ori=0,
                              color='white', colorSpace='rgb', opacity=1, languageStyle='LTR', depth=0.0)

# Random generation of trials
trial_sequence = data.TrialHandler(nReps=1, method='random', trialList=adjectives_combined.to_dict('records'), seed=None, name='trials')

def run_instructions():
    instructions.draw()
    win.flip()
    keys = event.waitKeys()  # Aspetta la pressione di un tasto per iniziare
    if 'escape' in keys:
        core.quit()

def run_trial(prime_text, bigsmall_value, congruent):
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

    # Presentazione del numero
    if congruent:
        if bigsmall_value == 1:
            number = random.choice([6, 7, 8, 9])  # Numeri maggiori di 5
        else:
            number = random.choice([1, 2, 3, 4])  # Numeri minori di 5
    else:
        if bigsmall_value == 1:
            number = random.choice([1, 2, 3, 4])  # Numeri minori di 5
        else:
            number = random.choice([6, 7, 8, 9])  # Numeri maggiori di 5

    number_stim.setText(str(number))
    number_stim.draw()
    win.flip()

    # Reset the clock to 0 when the target appears
    rt_clock = core.Clock()
    rt_clock.reset()

    # Record the response and reaction time
    response = event.waitKeys(keyList=['t', 'v', 'escape'])
    if 'escape' in response:
        core.quit()
    reaction_time = rt_clock.getTime()  # Get the time since the target appeared

    # Determine accuracy
    if (congruent and ((bigsmall_value == 1 and response[0] == 't') or (bigsmall_value == 0 and response[0] == 'v'))) or \
       (not congruent and ((bigsmall_value == 1 and response[0] == 'v') or (bigsmall_value == 0 and response[0] == 't'))):
        accuracy = '1'
    else:
        accuracy = '0'

    return response, reaction_time, accuracy

# Run the experiment
logging.console.setLevel(logging.WARNING)
trial_data = []

run_instructions()  # Visualizza le istruzioni all'inizio

for trial in trial_sequence:
    prime_text = trial['word']
    big_small_value = trial['bigsmall']
    congruent = trial['congruent'] == 1
    response, reaction_time, accuracy = run_trial(prime_text, big_small_value, congruent)
    trial_data.append((prime_text, big_small_value, congruent, response[0], reaction_time, accuracy))

# Save results
with open('data.csv', 'w') as data_file:
    data_file.write('prime,big_small,congruent,response,reaction_time,accuracy\n')
    for data_point in trial_data:
        data_file.write(f"{data_point[0]},{data_point[1]},{data_point[2]},{data_point[3]},{data_point[4]:.4f},{data_point[5]}\n")

win.close()
core.quit()
