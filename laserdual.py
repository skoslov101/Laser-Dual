
import os
import sys
import argparse
import numpy as np
import pandas as pd

from psychopy import visual, core, event


# handle input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--subj',default='s999',type=str,help='subject in s999 format')
args = parser.parse_args()


SUBJ = args.subj

# make a variable the tells program whether in "development" mode or not
DEV = True if SUBJ == 's999' else False


##  define parameters  ##

N_BLOCKS  = 4

# choose number of each trial type FOR A SINGLE BLOCK
N_TRIALS = dict(
    ax=20,
    ay= 5,
    bx= 5,
    by=20,
    ng=12,
)

N_TOTAL_TRIALS = sum(N_TRIALS.values())

# trial timing (all in seconds)
TIMES = dict(
    encoding = 0.5,
    delay    = 4.5,
    probe    = 0.5,
    iti      = 1.0, # response allowed during iti
)

# keyboard
QUIT_KEY = 'q'
BREAK_KEY = 'space'
RESP_KEYS = ['left','right',QUIT_KEY]



##  create master dataframe  ##

columns = ['subj','trialType','response','rt','accuracy']
index = pd.MultiIndex.from_product(
    [range(N_BLOCKS),range(N_TOTAL_TRIALS)],names=['block','trial'])
df = pd.DataFrame(columns=columns,index=index)

# Fill in the trialType columns with equal
# randomization of trials within each block.
# First make a big list of all the trial types,
# and then shuffle it and insert for each block.

tTypes_list = np.concatenate(
    [ np.repeat(k,v) for k, v in N_TRIALS.items() ])

for b in range(N_BLOCKS):

    # shuffle the trial types
    np.random.shuffle(tTypes_list)

    # PREVENT three consecutive same trial types
    threepeat = True
    while threepeat:
        np.random.shuffle(tTypes_list)
        for x, y, z in zip(tTypes_list,tTypes_list[1:],tTypes_list[2:]):
            if x == y == z:
                threepeat = True

    # insert the winner into dataframe for current block
    df.loc[b,'trialType'] = tTypes_list


# add subj to dataframe
df['subj'] = SUBJ



##  open psychopy window  ##

win = visual.Window(fullscr=DEV^1)

# create psychopy stims
cue_txtStim   = visual.TextStim(win)
probe_txtStim = visual.TextStim(win)
fixStim       = visual.TextStim(win, text='+++')
break_txtStim = visual.TextStim(win, text='Press space bar to continue. This yo brake.')
iti_txtStim   = visual.TextStim(win, text='+++')



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
#keys = psychopy.event.waitKeys(
#        keyList=["left", "right"],
#        timeStamped=clock
#        
#for key in keys:
#    if key[0] == "left":
#        key_num = 1
#    else:
#        key_num = 2
#        
#    responses.append([key_num, key[1]])
        
        
#    for j in range(N_MBLOCKS):
#        for k in range(N_TRIALS):
#            print (i,j,k)



#Byee##
#end(goodbye_text="Thank you for participating in our experiment!", goodbye_delay=5000)