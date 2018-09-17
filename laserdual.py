
from __future__ import absolute_import, division, print_function
from psychopy import locale_setup, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy import visual, core

# open window
win = visual.Window()

# Store info about the experiment session
expName = 'LaserDual' 
expInfo = {'participant': '', 'session': '001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  
expInfo['date'] = data.getDateStr()  # add timestamp
expInfo['expName'] = expName



######## open section to define a parameter
iti =  (5)
isi= (1)
N_BLOCKS = 4



#### create psychopy stims
## question equals what?
cue_txtStim = visual.TextStim(win)
probe_txtStim = visual.TextStim(win)
fixStim = visual.TextStim(win, text='+++')
breakTxtStim = visual.TextStim(win, text='Press space bar to continue. This yo brake.')
#probe_txtStim= probe

iti_txtStim=visual.TextStim(win, text='+++')

##Block param##
N_MBLOCKS = 20
PCT_AX = 0.4
PCT_AY = 0.1
PCT_BX = 0.1
PCT_BY = 0.4
PCT_NG = 0.2

N_TRIALS = 48 # per miniblock

NUM_AX = round(N_MBLOCKS*PCT_AX)
NUM_AY = round(N_MBLOCKS*PCT_AY)
NUM_BX = round(N_MBLOCKS*PCT_BX)
NUM_BY = round(N_MBLOCKS*PCT_BY)
NUM_NG = round(N_MBLOCKS*PCT_NG)

order = np.repeat('ax',NUM_AX)
order = np.append(order,np.repeat('ay',NUM_AY))
order = np.append(order,np.repeat('bx',NUM_BX))
order = np.append(order,np.repeat('by',NUM_BY))
order = np.append(order,np.repeat('ng',NUM_NG))


# keyboard setup parameters
QUIT_KEY = 'q'BREAK_KEY = 'space'RESP_KEYS = ['left','right',QUIT_KEY]


def generate_block():
    MINIBLOCKS_PER_BLOCK = 2
    total_order = np.array([])
    for block in range(MINIBLOCKS_PER_BLOCK):
        shuffle_order = order.copy()
        # shuffle order of categories within a run
        # prevent three consecutive category miniblocks
        threepeat = True
        while threepeat:
            threepeat = False
            np.random.shuffle(shuffle_order)
            for x, y, z in zip(shuffle_order,shuffle_order[1:],shuffle_order[2:]):
                if x == y == z:
                    threepeat = True
        total_order = np.append(total_order, shuffle_order)
    return total_order

#def check_if_order_valid(shuffle_order):
#    test_tuples = zip(shuffle_order,shuffle_order[1:],shuffle_order[2:])
#    for tup in range(len(shuffle_order)):
#        test_value = all(test_tuples[index]==np.repeat(test_tuples[index][0],3))
#        if test_value:
#            return False
#    return True


##############################################################
##  make keyboard functions to aid in collecting responses  ##
##############################################################



# run stuff#
def get_trial_parameters(trial_type):
    cue, probe = trial_type
    if trial_type == 'ax':
        answer = 'left'
    elif trial_type == 'ng':
        answer = None
    else:
        answer = 'right'
    return (cue, probe, answer)


#run_trial(trial_order[trial])
#def run_trial(trial_type):



### run through experiment
# loop through runs and trial

def run_trial(cue,probe):
    # show fixation (empty)
    fixStim.draw()
    win.flip()
    core.wait(1)
    # show cue
    cue_txtStim.text = cue
    cue_txtStim.draw()
    win.flip()
    core.wait(1)
    # show delay
    win.flip()
    core.wait(5)
    # show probe
    probe_txtStim.text = probe
    probe_txtStim.draw()
    win.flip()
    # response collection #
    response = event.waitKeys(maxWait=1,keyList=RESP_KEYS)
    if response == 'q':
        # quit program
        win.close(); sys.exit()
    elif response is not None:
        response = response[0]
        
    # iti
    iti_txtStim.draw
    win.flip()
    core.wait(1)
    
    return response

# initialize empty response list
response_list = []


## RUN EXPERIMENT ##
for i in range(N_BLOCKS):
    
    # wait for subj to continue
    breakTxtStim.draw()
    win.flip()
    event.waitKeys(keyList=BREAK_KEY)
    
    # generate random trial order
    trial_order = generate_block()
    
    # run through trials of the block
    for trial_type in trial_order:
        # get trial info
        cue, probe, answer = get_trial_parameters(trial_type)
        # run single trial
        response = run_trial(cue,probe)
        # add response to list of responses
        response_list.append(response)
        print(response_list)
        
#    return answer
   
#        
#keys = psychopy.event.waitKeys(#        keyList=["left", "right"],#        timeStamped=clock
#        
#for key in keys:#    if key[0] == "left":#        key_num = 1#    else:#        key_num = 2
#        #    responses.append([key_num, key[1]])
        
        
#    for j in range(N_MBLOCKS):
#        for k in range(N_TRIALS):
#            print (i,j,k)



#Byee##
#end(goodbye_text="Thank you for participating in our experiment!", goodbye_delay=5000)