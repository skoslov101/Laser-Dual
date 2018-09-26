import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

'''
data frame look like dis: 
columns = ['subj','trialType','cue','probe','response','rt','accuracy']
'''
#########################
working function to graph 
RT by trialtype!!!
#########################

from Laser-Dual import data
dataframe = pd.read_csv('data.csv')
grouped_df = dataframe.groupby(['trialType'])
print grouped_df['rt'].describe().unstack()

viol_ax = sns.violinplot(x="trialType", y="rt", palette='colorblind',
data=dataframe)
 
save_fig = viol_ax.get_figure()
plt.show()

#################################

##How many samples from distributution
nsamples= 50

samples = np.random.poisson(lam=4, size=n_samples)


##for histogram bin locations on x axis and the bin counts on the yaxis##

bin_counts = np.bincount(samples)

bins = np.arange(np.max(samples) + 1)

## veusz is a plotter which plots a function on the graph
embed = veusz.embed.Embedded("veusz")

page = embed.Root.Add("page")
page.width.val = "8.4cm"
page.height.val = "6cm"

##autoadd false because we will create the axes in the graph ourselves.
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




##comparing 2sample t test 
n_per_group = 30

# effect size = 0.8
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

