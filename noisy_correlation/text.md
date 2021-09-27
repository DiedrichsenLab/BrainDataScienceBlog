# How can we calculate the true correlation between two activity patterns? 

# What is the *true* correlation between two activity patterns? 
<section markdown="1">
In neuroimaging, we often want to know how similar, or overlapping, two brain activity patterns are. If two tasks (let's call them *A* and *B*) activate a specific brain region in a similar way, we can infer that this brain region does something similar in the two conditions. If the activations are very different, we can conclude that this brain region does something quite dissimilar in the two situations. Often, we are not so concerned with the question whether task *A* activates the brain region more than task *B* - rather we want to know whether the *pattern* of activation across the brain's surface is the same or not - that is, we are interested in the *correlation* between the two activity patterns. 
{+margin:m1:Of course, sometimes we do care about the amount of activation, in which case correlations are not the right measure. But that's a topic for another blog.}
The question of the correlation between two activations patterns re-occurs over and over. How much does encoding and retrival of the same item lead to similar activity pattterns? How about planning and execution of the same movement? Or does the pattern related to a specific movement change with training?

## So what's the problem? 
Statistically speaking, we are interested in the correlation between two vectors  $\mathbf{x}_A$ and $\mathbf{x}_B$.  Easy, you may say. Just correlate the two vectors! But here is the hitch: we don't actually have the true activity patterns. Rather, we measure each of the patterns with noise - and if we use functional magnetic resonance imaging (fMRI), we have lot of it! Graphically, we can represent the situation as such (Figure 1). We are interested in the correlation between two true (but unobservable) activation patterns  $\mathbf{x}_A$ and $\mathbf{x}_B$.  We have a range of observations of each activity pattern  $\mathbf{y}_{a,1}, \mathbf{y}_{a,2},...$ which differ from the true patterns by the measurement noise. 

![Alternative](Figure_1.png)**Figure 1.** Graphical model representation of measurement problem. Observed variables are represented in shaded circles, unobserved variables in empty circles. Correlations are represented with undirected edges. The measures are dependent on the true patterns (arrows), but are conditionally independent of each other. 

The obvious way to go about this, is of course to average the patterns across our measurements for the two tasks, resulting in $\bar{\mathbf{y}}_a$ and $\bar{\mathbf{y}}_b$, and then just correlate those me an patterns. The problem is that the empirical correlation underestimates the true correlation substantially. This can be seen in Figure 2, which shows a simulation of exactly this phenomon. The individual measured correlations (green dots) tend to be below the true correlation (dashed line).  As the signal / noise ratio decreases, this bias becomes more severe. In the extreme, when we have no signal, the correlation will go down to zero. 

![Alternative](Figure_1.html)**Figure 2.** Normal correlation estimates (dots) systematically underestimate the true correlation (dashed line) in a signal-dependent fashion. See this notebook to play around with this simulation. 

This is not a problem, if we just want to test the hypothesis that the true correlation is larger than zero ($r>0$). Just calculate the individual correlations per subject and test them against zero using a *t-*test. However, sometimes we want to test whether the true correlation has a specific value (for example $r=1$, indicting that the activity patterns are the same), or we want to test whether the correlations are higher in one brain region than another. Brain regions measured with fMRI can often differ dramatically in their signal-to-noise ratio. Thus, in these cases we need to take account the problem of measurement noise. 
</section>
<section markdown="1">
## Solution 1a: Compute noise ceilings


## Solution 1b: Use  cross-block covariances

</section>
<section markdown="1">
## Solution 2: Using a Bayesian approach (Pattern Component Modelling) 


## Dealing with more complex situations
</section>
