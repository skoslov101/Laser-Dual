
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
DEV = True if SUBJ in ['s999','sim'] else False

##  io  ##

data_fname = './data/{:s}_data.csv'.format(SUBJ)

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

N_BLOCK_TRIALS = sum(N_TRIALS.values()) # per block

# trial timing (all in seconds)
TIMES = dict(
    fixation = 0.5,
    cue      = 0.5,
    delay    = 4.5,
    probe    = 1.5,
    feedback = 0.5,
    iti      = 1.0, 
)

# make experiment fast if subj == 'sim'
TIMES = { k: v/100 for k, v in TIMES.items() }

# keyboard
QUIT_KEY = 'q'
BREAK_KEY = 'space'
RESP_KEYS = ['left','right',QUIT_KEY]



##  create master dataframe  ##

columns = ['subj','trialType','cue','probe','response','rt','accuracy']
index = pd.MultiIndex.from_product(
    [range(N_BLOCKS),range(N_BLOCK_TRIALS)],names=['block','trial'])
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
        threepeat = False
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
fixStim       = visual.TextStim(win, text='+')
break_txtStim = visual.TextStim(win, text='Press space bar to continue. This yo brake.')
fdbck_txtStim = visual.TextStim(win, text='+++')
iti_txtStim   = visual.TextStim(win, text='+++')



##############################################################
##  make keyboard functions to aid in collecting responses  ##
##############################################################


# define function used to run a single trial
def run_trial(run_num,trial_num):

    # extract the trial type from master dataframe
    trial_type = df.loc[(run_num,trial_num),'trialType']
    # break apart the trial type into cue and probe
    # (eg, break AX into A and X)
    if trial_type == 'NG':
        cue = np.random.choice(['A','B'])
        probe = np.random.choice([1,2,3,4,5,6,7,8,9])
    else:
        cue, probe = trial_type

    # change cue/probe sometimes on AY and BX trials
    if trial_type == 'AY':
        # keep probe but change cue
        cue = np.random.choice(['A','E','G','P','R','S'])
    elif trial_type == 'BX':
        # keep cue but change probe
        probe = np.random.choice(['X','F','J','M','Q','U'])

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
    probe_txtStim.draw()
    win.flip()
    response = None
    t0 = core.getTime()
    response = event.waitKeys(maxWait=TIMES['probe'],keyList=RESP_KEYS,timeStamped=True)

    # handle response
    if response is None:
        char, rt = np.nan, np.nan
        acc = True if trial_type == 'NG' else False
    else:
        char, time = response[0]
        if char == 'q':
            sys.exit() # quit
        rt = time - t0
        acc = True if char == answer else False

    # show feedback
    feedback_color = 'green' if acc else 'red'
    fdbck_txtStim.setColor(feedback_color)
    fdbck_txtStim.draw()
    win.flip()
    core.wait(TIMES['feedback'])

    # show iti
    iti_txtStim.draw()
    win.flip()
    core.wait(TIMES['iti'])

    # insert trial results into master dataframe
    df.loc[(run_num,trial_num),['response','rt','accuracy']] = (char,rt,acc)
    # insert unique cue/probe into master dataframe
    df.loc[(run_num,trial_num),['cue','probe']] = (cue,probe)



##  RUN EXPERIMENT  ##
for b in range(N_BLOCKS):
    
    # wait for subj to continue
    break_txtStim.draw()
    win.flip()
    response = event.waitKeys(keyList=[BREAK_KEY,QUIT_KEY])
    if QUIT_KEY in response:
        sys.exit()
        
    # run through trials of the block
    for t in range(N_BLOCK_TRIALS):
        run_trial(b,t)
        # save after every trial
        df.to_csv(data_fname,na_rep=np.nan)



#Byee##
break_txtStim.text = 'Byee'
break_txtStim.draw()
win.flip()
core.wait(2)
