'''
Hello. This is the display script for laserdual.

To run a subject, move to this directory
and call this script from terminal with:

$ python laserdual.py --subj <subject_id>

(subject_id should be in s999 format)

To run a demo, use subject_id s999.
To run a supafast simulated version, use subject_id sim.
'''

from __future__ import print_function

import os
import sys
import requests
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
dropbox_fname = '~/DropBox (LewPeaLab)/BEHAVIOR/LaserDual{:s}_data.csv'.format(SUBJ)


#########################
##  define parameters  ##
#########################

N_BLOCKS  = 4

# choose number of each trial type FOR A SINGLE BLOCK
N_TRIALS = dict(
    AX=16,
    AY= 4,
    BX= 4,
    BY=16,
    NG=8,
)

N_BLOCK_TRIALS = sum(N_TRIALS.values()) # per block

# trial timing (all in seconds)
TIMES = dict(
    fixation = 0.5,
    cue      = 0.5,
    delay    = 3.5,
    probe    = 0.5,
    probe2   = 1.0,
    feedback = 1.5,
    iti      = 1.0, 
)

# make experiment fast if subj == 'sim'
if SUBJ == 'sim':
    TIMES = { k: v/100 for k, v in TIMES.items() }

# keyboard
QUIT_KEY = 'q'
BREAK_KEY = 'space'
RESP_KEYS = ['left','right',QUIT_KEY]

# slack
SLACK = dict(
        channel='#laserdual-exp',
        botname='{:s}'.format(SUBJ),
        emoji=':lightsaber:',
        url='https://hooks.slack.com/services/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'
    ) if not DEV else None


###############################
##  create master dataframe  ##
###############################

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


############################
##  open psychopy window  ##
############################

win = visual.Window(fullscr=DEV^1)

# create psychopy stims
cue_txtStim   = visual.TextStim(win, height=0.3, color='blue', bold=True)
probe_txtStim = visual.TextStim(win, height=0.3, bold=True)
probe2_txtStim = visual.TextStim(win, text='+++', height=0.3)
fixStim       = visual.TextStim(win, text='+', height=0.3)
break_txtStim = visual.TextStim(win, text='Press space bar to continue.')
fdbck_txtStim = visual.TextStim(win, text='+++', height=0.3)
iti_txtStim   = visual.TextStim(win, text='+', height=0.3)


##################################
##  define experiment functions ##
##################################

# define function used to run a single trial
def run_trial(run_num,trial_num):

    # extract the trial type from master dataframe
    trial_type = df.loc[(run_num,trial_num),'trialType']
    # break apart the trial type into cue and probe
    # (eg, break AX into A and X)
    if trial_type == 'NG':
        cue = ngList.pop(0)
        probe = np.random.choice([1,2,3,4,5,6,7,8,9])
    else:
        cue, probe = trial_type

    # change cue/probe sometimes on AY and BX trials
    if trial_type == 'AY':
        # keep probe but change cue
        probe = np.random.choice(['F','J','M','Q','U'])
    
    elif trial_type == 'BX':
        # keep cue but change probe
        cue = np.random.choice(['E','G','P','R','S'])
    elif trial_type == 'BY':
        cue = np.random.choice(['E','G','P','R','S'])
        probe = np.random.choice(['F','J','M','Q','U'])

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
        # char, rt = np.nan, np.nan
        # acc = True if trial_type == 'NG' else False
        # second half of probe period
        probe2_txtStim.draw()
        win.flip()
        response = event.waitKeys(maxWait=TIMES['probe2'],keyList=RESP_KEYS,timeStamped=True)
        if response is None:
            char, rt = np.nan, np.nan
            acc = True if trial_type == 'NG' else False
        else:
            char, time = response[0]
            if char == 'q':
                sys.exit() # quit
            rt = time - t0
            acc = True if char == answer else False
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


def slackit(msg):
    print(msg)
    if SLACK:
        payload = dict(text=msg,channel=SLACK['channel'],username=SLACK['botname'],icon_emoji=SLACK['emoji'])
        try: requests.post(json=payload,url=SLACK['url'])
        except ConnectionError: print('Slack messaging failed--no internet connection.')


######################
##  RUN EXPERIMENT  ##
######################

slackit('Started experiment.')

for b in range(N_BLOCKS):

    noB=np.random.choice(['E','G','P','R','S'],4,replace=False)
    ngList=np.append(noB, ['A', 'A', 'A', 'A'])
    np.random.shuffle(ngList)
    ngList=list(ngList)

    
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
        df.to_csv(dropbox_fname,na_rep=np.nan)

    # send end of block slack message
    slackit('Finished block {:d}'.format(b+1))



############
##  Byee  ##
############



break_txtStim.text = 'Thanks for participating in the study. Please return to experimenter.'

break_txtStim.draw()
win.flip()
core.wait(2)

