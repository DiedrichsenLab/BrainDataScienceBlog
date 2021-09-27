# How can we calculate the true correlation between two activity patterns? 

# What is the *true* correlation between two activity patterns? 
<section markdown="1">

In neuroimaging, we often want to know how similar, or overlapping, two brain activity patterns are. If two tasks (let's call them $A$ and B) activite a specific brain region in a similar way, then we can infer that this brain region does something similar in the two conditions. If the activations are non-overlapping or very different, we could conclude that this brain region does something quite dissimilar in the two situations. Often, we are not so concerned with the question whether task A activates the brain region more than task B - rather we want to know whether the*pattern* of activation across the brain's surface is the same or not - that is, we are interested in the *correlation* between the two activity patterns. 
{+margin:m1:Of course, sometimes we do care about the amount of activation, in which case correlations are not the right measure. But that's a topic for another blog.}
Thus, the question of the correlation between two activations patterns re-occurs over and over. How much does encoding and retrival of the same item lead to similar activity pattterns? How about planning and execution of the same movement? Or does the pattern related to a specific movement change with training?

## So what's the problem? 

Thus, statistically speaking, we are interested in the correlation between two vectors  $\mathbf{x}_A$ and $\mathbf{x}_B$.  Easy, you may say, just correlate the two vectors! True, but here is the hitch: we don't actually have the true activity patterns. Rather, we measure each of the patterns with measurement noise - and if we use functional magenetic resonance imaging, we have lot of it! Graphically, we can represent the situation as such (see Figure 1). We are interested in the correlation between the two true (but unobservable) activation patterns  $\mathbf{x}_A$ and $\mathbf{x}_B$. Because the correlation does not imply a causal direction, we have represented it in an undirected edge. What we can observe are different measures  $\mathbf{y}_{a,1}, \mathbf{y}_{a,2},...$ that of course depend on the true pattern $\mathbf{x}_a$, but are otherwise independent from other measures.
{+side:s1:These so-called conditional independence is crucial and can be expressed in the graphical model notion. See more at.}
The main problem is that the measured patterns differ from the true patterns by the measurement noise. 

$$
\mathbf{y}_{a,1} =\mathbf{x}_{a} + \boldsymbol{\epsilon}_{a,1}
$$

![Alternative](Figure_1.png)

The obvious way to go about this, is of course to average the patterns across our measurements for the two tasks, resulting in $\bar{\mathbf{y}}_a$ and $\bar{\mathbf{y}}_b$, and then just correlated those me an patterns. The problem is that the empirical correlation underestimates the true correlation substantially. This can be seen in Figure 2, which shows a simulation{+side:s2:see this jupyter notebook} of exactly this phenomon. The individual measured correlations (green dots) tend to be below the true correlation (dashed line). Indeed, the mean is substantial below the line. As the signal / noise ratio decreases, the bias becomes more severe. In the extreme, when we have no signal, the correlation will go down to zero {+side:s3:This of course assumes that the noise is uncorrelated across all observations - see more below}. 

So, again, is this a problem? 





The whole situation is shown in Figure 1 in a so-called graphical model. A circle here refer to the whole region- or even brain-wide pattern. Filled circles we can observe, whereas unfilled circles we cannot observe. We are interested in the correlation (represented by the undirected edge) between 



![REF](Figure_1.html)

 

This question Problem...
Of course we can 

Well, not if you just want to show that the random vectos )
</section>

<section markdown="1">
## Solution 1: Correcting for noise by using cross-block covariances (or split-half correlations)


## Solution 2: Using a Bayesian approach (Pattern Component Modelling) 


## How to deal with more complex situations
</section>
