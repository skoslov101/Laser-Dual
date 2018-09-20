
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
    AX=20,
    AY= 5,
    BX= 5,
    BY=20,
    NG=12,
)

N_TOTAL_TRIALS = sum(N_TRIALS.values())

# trial timing (all in seconds)
TIMES = dict(
    fixation = 0.5,
    cue      = 0.5,
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

def run_trial(run_num,trial_num):

    # extract the trial type from master dataframe
    trial_type = df.loc[(run_num,trial_num),'trialType']
    # break apart the trial type into cue and probe
    # (eg, break AX into A and X)
    cue, probe = trial_type

    # choose the correct answer for the trial
    if trial_type == 'AX':
        answer = 'left'
    elif trial_type == 'NG':
        answer = None
    else:
        answer = 'right'

    # change the cue and probe stims to have right text
    cue_txtStim.text = cue
    probe_txtStim.text = probe

    # reset the color of iti stim (bc it changes with response feedback)
    iti_txtStim.setColor('white')

    # show fixation
    fixStim.draw()
    win.flip()
    core.wait(TIMES['fixation'])
    # show cue
    cue_txtStim.draw()
    win.flip()
    core.wait(TIMES['cue'])
    # show delay
    win.flip()
    core.wait(TIMES['delay'])

    # show probe and collect response
    response = None
    t0 = core.getTime()
    while core.getTime()-t0 < TIMES['probe']+TIMES['iti']:
        if (response is None) and (core.getTime()-t0 < TIMES['probe']):
            probe_txtStim.draw()
        else:
            iti_txtStim.draw()

        if response is None:
            ### THIS IS BAD BC RTS WILL NOT BE CONTINUOUS
            response = event.getKeys(keyList=RESP_KEYS)[0]
            # handle response
            if response == 'q':
                sys.exit() # quit program
            elif response == answer:
                acc = True
                iti_txtStim.setColor('green')
            else:
                acc = False
                iti_txtStim.setColor('red')

        win.flip()

    # handle situation when that didn't respond
    if response is None:
        if trial_type == 'NG':
            acc = True:
        else:
            acc = False

    # save response into master dataframe
    df.loc[(run_num,trial_num),['respose','rt','accuracy']] = (response,rt,acc)



##  RUN EXPERIMENT  ##
for i in range(N_BLOCKS):
    
    # wait for subj to continue
    break_txtStim.draw()
    win.flip()
    event.waitKeys(keyList=BREAK_KEY)
        
    # run through trials of the block
    for b in range(N_BLOCKS):
        for t in range(N_TOTAL_TRIALS):
            run_trial(b,t)


#Byee##
#end(goodbye_text="Thank you for participating in our experiment!", goodbye_delay=5000)