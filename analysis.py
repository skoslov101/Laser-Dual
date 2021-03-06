import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
<<<<<<< HEAD
from scipy.stats import t
=======
>>>>>>> d7ec4a501a1d516953bbb44d3f8a1ad6f6d99dfc

'''
data frame look like dis: 
columns = ['subj','trialType','cue','probe','response','rt','accuracy']
'''
<<<<<<< HEAD

from Laser-Dual import data

#########
##TTEST##
#########


def paired_ttest(x, y): 
## x = laser
## y = sham
    diff = [] 
    n = len(x)
for i in range(n):
	diff.append(x[i] - y[i])
	dbar = float(sum(diff))/n
	sd = 0.

 #subj difference in score subtracted by the av and **

for d in diff:
    sd += (d-dbar)**2
    sd_diff = np.sqrt(std_di/n)
#SE of mean
    se_dbar = sd_diff/np.sqrt(n-1)
    t_val = dbar/se_dbar
    pval = t.sf(np.abs(t_val), df) * 2
 
    stats = {'T-value':t_val, 'degree of freedom':df, 'P-value':pval}
 
    return stats

#create dataframe = df
df = pd.read_csv('{:s}_data.csv')
grouped_df = df.groupby(['trialType'])
print grouped_df['rt'].describe().unstack()

viol_ax = sns.violinplot(x="trialType", y="rt", palette='colorblind',
data=df)
=======
#########################
working function to graph 
RT by trialtype!!!
#########################

from Laser-Dual import data
dataframe = pd.read_csv('{:s}_data.csv')
grouped_df = dataframe.groupby(['trialType'])
print grouped_df['rt'].describe().unstack()

viol_ax = sns.violinplot(x="trialType", y="rt", palette='colorblind',
data=dataframe)
>>>>>>> d7ec4a501a1d516953bbb44d3f8a1ad6f6d99dfc
 
save_fig = viol_ax.get_figure()
plt.show()


viol_acc = sns.violinplot(x="trialType", y="accuracy", palette='colorblind',
<<<<<<< HEAD
data=df)
=======
data=dataframe)
>>>>>>> d7ec4a501a1d516953bbb44d3f8a1ad6f6d99dfc


#Group data by trial type & subject number. 
#Then get mean RT for the trial types
<<<<<<< HEAD
grouped_sub = df.groupby(['trialType', 'subj'])
means = grouped_sub['rt'].mean()

# Assign RT values to x and y
x, y = means['AX'].values, means['BX'].values

=======
grouped_sub = dataframe.groupby(['trialtype', 'SUBJ'])
means = grouped_sub['RT'].mean()

# Assign RT values to x and y
x, y = means['incongruent'].values, means['congruent'].values
>>>>>>> d7ec4a501a1d516953bbb44d3f8a1ad6f6d99dfc
t_value = paired_ttest(x, y)


# loop through t-value
for key, value in t_value.iteritems():
    t_value[key] = round(value, 3)
 
print t_value

#################################

'''
what measures do we want - 
NEED 2 BRUSHUP STATS STAT.

1. PBI = (AY-BX)/(AY+BX)
	- measure of the interference during AY and BX trials.

2. A-cue bias = 1/2*(Z[H] + Z[F])
	- provide a measure of the tendency of participants to make a target response after an A cue

3. d’-context = hits on AX trials and false alarms on BX trials (Z(H) - Z(F))
	- measure the ability of participants to employ contextual information from the cue to guide their answer to the probe.
'''


## number of samples from distributution
nsamples= 50

samples = np.random.poisson(lam=4, size=n_samples)


##for histogram bin locations on x axis and the bin counts on the yaxis##

bin_counts = np.bincount(samples)

bins = np.arange(np.max(samples) + 1)

## veusz is a plotter which plots a function on the graph
embed = veusz.embed.Embedded("veusz")

#page = embed.Root.Add("page")

##autoadd false because we will create the axes in the graph manually.
graph = page.Add("graph", autoadd=False)

x_axis = graph.Add("axis")
y_axis = graph.Add("axis")

bar = graph.Add("bar")

embed.SetData("bins", bins)
embed.SetData("bin_counts", bin_counts)

##set the bar variable to the names given to bin location and bin count data respectively

bar.posn.val = "bins"
bar.lengths.val = "bin_counts"


x_axis.label.val = "Value"
y_axis.label.val = "Count"

<<<<<<< HEAD
=======



##comparing 2sample t test 
n_per_group = 25

# effect size = tbd
group_means = [0.0, 0.8]
group_sigmas = [1.0, 1.0]

n_groups = len(group_means)

data = np.empty([n_per_group, n_groups])
data.fill(np.nan)

for i_group in range(n_groups):

    data[:, i_group] = np.random.normal(
        loc=group_means[i_group],
        scale=group_sigmas[i_group],
        size=n_per_group)

assert np.sum(np.isnan(data)) == 0


embed.WaitForClose()

>>>>>>> d7ec4a501a1d516953bbb44d3f8a1ad6f6d99dfc
