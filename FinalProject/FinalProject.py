# "Your comments at the start of the code should include the name of the file, an explanation of what your experiment does and why, and your name."
            # Name of file is FinalProject.py or if you meant the output example file, it is Sub1_14-12-2022_outputFile
            # Experiment is a varation of the Stroop Task, measures selective attention. Why? beacuse this is the topic I chose. See more in the readme file.
            # My name is Amanda

#================
#IMPORT MODULES
#================
from psychopy import event, visual, monitors, core, gui
     #"event" allows you to collect responses
     #"visual" allows you to draw various stimuli
     #"monitors" allows you to change your settings
     #"core" contains various functions used for timing, waiting, and quitting the experiment
     # "gui" (graphical user interface) allows you to create a dialog box to collect participant information

from datetime import datetime # Allows you to manipulate dates and time
import pandas as pd # Used to help with data analysis
import numpy as np # Used to help calculate/manipulate numbers
import random # Can use to shuffel, randomize numbers, stimuli etc.
import csv # Allows user to save code in excel form
import os # Allows you to define and change the current working directory, and list files in a directory etc.

#=====================
#PATH SETTINGS
#=====================
main_dir = os.getcwd() # Get path from current working directory
data_dir = os.path.join(main_dir,'data') # 'data' - the name of the folder where my data will be kept
if not os.path.exists(data_dir): # If path doesn't exist, make one
    os.makedirs(data_dir)

#==========================
#COLLECT PARTICIPANT INFO
#==========================
# Make gui 
exp_info = {'subject_nr':0, # The range of my variables
            'age':0, 
            'handedness':('right','left','ambi'), 
            'gender':('female','male','other','prefer not to say'),
            'session': 1}

expInfo = 0
while expInfo == 0: # To prompt the user again after an error

    my_dlg = gui.DlgFromDict(dictionary=exp_info, # How I want the variables to look in the pop-up box
                            title='subject info',
                            fixed=['session'],
                            order=['session', 'subject_nr', 'age', 'gender', 'handedness'])
    # Make sure subject data is entered correctly
    if exp_info['subject_nr'] ==0: # If nothing is entered, give error message
        err_dlg = gui.Dlg(title='error message') # Give the dlg a title
        err_dlg.addText('Enter a valid subject number!') # Create an error message
        err_dlg.show() # Show the dlg
    else:
        expInfo = 1
        
    # Make sure subject can consent to taking part in the experiment        
    if exp_info['age'] < 18: # If under the age of 18
        err_dlg = gui.Dlg(title='error message')
        err_dlg.addText('%d year olds cannot give consent!' % (exp_info['age'])) # Error Message
        err_dlg.show() # Show message
        core.quit()
    
# What time is it right now?
date = datetime.now()
exp_info['date'] = str(date.day) + '-' + str(date.month) + '-' + str(date.year)
print(exp_info['date'])

# Create a unique filename for the data
filename = ('Sub' + str(exp_info['subject_nr']) + '_' + exp_info['date'] + '_outputFile.csv')
fullAddress = os.path.join(data_dir, filename)
print(fullAddress) # To make sure it's where I want it to be

# Monitor Settings
mon = monitors.Monitor('myMonitor', width=14.2, distance=8) 
mon.setSizePix([1366,768])

# Pop-up Window settings
win = visual.Window(monitor=mon, size=(600,600), units="pix", fullscr=False, color=[-1,-1,-1])

#=====================
#STIMULUS AND TRIAL SETTINGS
#=====================
# Define blocks, trials, stims, and clocks
nBlocks=3
nTrials=6
totalTrials = nTrials*nBlocks
nEach = int(totalTrials/2)

blocks = [[0, 0, 0, 0], [1, 1, 1, 1], [2, 2, 2, 2]] 
trials = [[0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5]] 
my_text=visual.TextStim(win)
rt_clock = core.Clock()  # Create a response time clock
cd_timer = core.CountdownTimer() # Add countdown timer

# Define the stimulus
stims = ['Left', 'Right']*nEach # Prompt word

for stim in stims:
    colour = ['green']*nEach + ['red']*nEach # Instruction on which direction to press

trials = list(zip(stims, colour))
np.random.shuffle(trials)

#=====================
#PREPARE DATA COLLECTION LISTS
#=====================
# Create an empty list for:
colours = [0]*totalTrials # Colours - part of the noise, used as instrutions for the words
acc_resp = [0]*totalTrials # Accurancy Response - correct or incorrect
resp_times = [0]*totalTrials # Response Times
trialNumbers = [0]*totalTrials 
blockNumbers = [0]*totalTrials
corr_resp = [0]*totalTrials # Correct Responses - Left or Right
stims = [0]*totalTrials

#=====================
#START EXPERIMENT
#=====================
# Present start message text
start_msg = "Welcome to Coloured Directions! Press any key to begin" 
start_text = visual.TextStim(win, text = start_msg) # Define experiment start text using psychopy functions

start_text.color = ['white'] # The highlight of the message
start_text.draw() # Executes the code inside the block until told otherwise
start_text.color = ['cadetblue'] # Main colour of the message
start_text.pos = [1, 1] # Shift the white text one pixel to the right and one pixel up to create a bold or shadow effect
start_text.draw() 
win.flip() # To dispay the message.
event.waitKeys() # Allow participant to begin experiment with button press

#Instructions
instr_msg = "When the word is green, using the arrow keys, press the direction of the word. When the word is red, press the opposite of the word. Press any key to continue"
instr_text = visual.TextStim(win, text = instr_msg)
instr_text.color = ['gray']
instr_text.draw() 
win.flip() 
event.waitKeys()

#=====================
#BLOCK SEQUENCE
#=====================
trial_timer = core.Clock()

for iblock in range(nBlocks):
    block_msg = 'Press any key to continue to block' + ' ' + str(iblock+1) # Message + counts the blocks
    block_text = visual.TextStim(win, text = block_msg)
    block_text.color = ['gray']
    block_text.draw()
    win.flip() 
    event.waitKeys() 
    
    np.random.shuffle(stims) # Randomize order of trials 
    
    for itrial in range(nTrials):        
        # Defining variables
        overallTrial = iblock*nTrials+itrial
        blockNumbers[overallTrial] = iblock+1
        trialNumbers[overallTrial] = itrial+1
        colours[overallTrial] = trials[overallTrial][1]
        
        stim_text = visual.TextStim(win, text=trials[overallTrial][0]) #stims = left and right
        stim_text.color = trials[overallTrial][1] 
        stim_text.draw()
        trial_timer.reset() # Reset response time clock so every trial's duration is recorded individually
        win.flip() 
            
        keys=event.waitKeys(keyList=['left','right']) # Only these keys will be recorded
        resp_times[overallTrial] = trial_timer.getTime() 
            
        # If statement runs if condition is true, if false the else statement will run
        if keys:
            if trials[overallTrial][1] == 'green':
                # Uses a boolean function to say if keys = 0 its correct for green, else it's incorrect etc.
                # Also gathering correct responses for excel
                if keys[0] == 'left':
                    acc_resp[overallTrial] = 'Correct'
                    corr_resp[overallTrial] = 'Left'
                else:
                    acc_resp[overallTrial] = 'Incorrect'
                    corr_resp[overallTrial] = 'Left'
            else:
                if keys[0] == 'right':
                    acc_resp[overallTrial] = 'Correct'
                    corr_resp[overallTrial] = 'Right'
                else: 
                    acc_resp[overallTrial] = 'Incorrect'
                    corr_resp[overallTrial] = 'Right'
                
#==============
#END TRIAL
#============== 
# Define end trial text
end_msg = "End of Experiment! Press any key to close"
end_text = visual.TextStim(win, text = end_msg)# Define stimuli using psychopy functions

# Making the same shadow effect as the start message
end_text.color = ['white']
end_text.draw()
end_text.color = ['cadetblue']
end_text.pos = [1, 1]
end_text.draw()

win.flip() 
event.waitKeys()     
# Close experiment
win.close() 

#===========================================================
 # Prints output as a table
print(
    'Block:',
    iblock+1,
    ', Trial:', 
    itrial+1, 
    ',', 
    trials[overallTrial][1], 
    ':',
    corr_resp[overallTrial],
    ',',
    acc_resp[overallTrial], 
    ', RT:', 
    resp_times[overallTrial]
    )

# Recipe to make a dict of objects in columns look pretty in a spreadsheet.
df = pd.DataFrame(data={
 "Block Number": blockNumbers, 
 "Trial Number": trialNumbers, 
 "Colour": colours,
 "Correct Response": corr_resp,
 "Accuracy": acc_resp, 
 "Response Time": resp_times
})
df.to_csv(os.path.join(fullAddress), sep=',', index=False)

# Closes the window
win.close()