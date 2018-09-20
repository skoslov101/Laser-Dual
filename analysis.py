import numpy as np


nsamples= []

samples = np.random.poisson(lam=4, size=n_samples)

bin_counts = np.bincount(samples)

bins = np.arange(np.max(samples) + 1)

embed = veusz.embed.Embedded("veusz")

page = embed.Root.Add("page")
page.width.val = "8.4cm"
page.height.val = "6cm"

graph = page.Add("graph", autoadd=False)

x_axis = graph.Add("axis")
y_axis = graph.Add("axis")

bar = graph.Add("bar")

embed.SetData("bins", bins)
embed.SetData("bin_counts", bin_counts)

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


embed.WaitForClose(

