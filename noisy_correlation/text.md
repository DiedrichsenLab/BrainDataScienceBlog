# How can we estimate the *true* correlation between two activity patterns? 


<section markdown="1">
In neuroimaging, we often want to know how similar, or overlapping, two brain activity patterns are. If two tasks (let's call them *A* and *B*) activate a specific brain region in a similar way, we can infer that this brain region does something similar in the two conditions. Often, we are not so much concerned with whether task *A* activates the region more than task *B* - rather we want to know whether the *pattern* of activation across the brain's surface is the same or not - that is, we are interested in the *correlation* between the two activity patterns. 
{+margin:Of course, sometimes we do care about the amount of activation, in which case correlations are not the right measure. But that's a topic for another blog.}
The question of the correlation between two activations patterns comes up a lot. Does encoding and retrieval of the same item lead to similar activity patterns? To what degree do the activity patterns during planning and execution overlap? How much does a pattern related to a specific movement change with training [+citep:Berlot2020]? Estimating the true correlation between two patterns, however, can be extremely tricky.


## So what's the problem? 
Statistically speaking, we are interested in the correlation between two vectors  $\mathbf{x}_A$ and $\mathbf{x}_B$.  Easy, you may say - just correlate the two vectors. But here is the hitch: we don't actually have the true activity patterns. Rather, we measure each of the patterns with noise - and if we use functional magnetic resonance imaging (fMRI), we have lot of it. Graphically, we can represent the situation as depicted in Figure 1. We are interested in the correlation between two true (but unobservable) activation patterns  $\mathbf{x}_A$ and $\mathbf{x}_B$.  We have a range of observations of each activity pattern  $\mathbf{y}_{a,1}, \mathbf{y}_{a,2},...$ which differ from the true patterns by the measurement noise. 

![Alternative](Figure_1.png)**Figure 1.** Graphical model representation of our measurement problem. Observed variables are represented in shaded circles, unobserved variables in empty circles. Correlations are represented with undirected edges. The measures are dependent on the true patterns (arrows), but are conditionally independent of each other [(Jordan, 2003)](https://people.cs.pitt.edu/~milos/courses/cs3750-Spring2020/Readings/Graphical_models/chapter2.pdf).

The obvious way to go about this, is to average the patterns across our measurements for the two tasks, resulting in $\bar{\mathbf{y}}_a$ and $\bar{\mathbf{y}}_b$, and then just correlate those mean patterns. However, the problem is that the empirical correlation underestimates the true correlation substantially. This phenomenon can be seen in simulation in Figure 2. The individual measured correlations (green dots) tend to be below the true correlation (dashed line).  As the signal / noise ratio decreases, this bias becomes more severe. In the extreme, when we have no signal and the correlation goes down to zero. 

![Alternative](Figure_2.html)**Figure 2.** Normal correlation estimates (dots) systematically underestimate the true correlation (dashed line). See this [Jupyter notebook](https://github.com/DiedrichsenLab/BrainDataScienceBlog/blob/main/noisy_correlation/correlation_demo.ipynb) for details for this simulation. 

This is not a problem if we just want to test the hypothesis that the true correlation is larger than zero ($r>0$). We can just calculate the individual correlations per subject and test them against zero using a *t-*test. However, sometimes we want to test whether the true correlation has a specific value (for example $r=1$, indicting that the activity patterns are the same), or we want to test whether the correlations are higher in one brain area than another. Brain regions measured with fMRI often differ dramatically in their signal-to-noise ratio. Thus, in these cases we need to take into account our level of measurement noise. 
</section>

<section markdown="1">

## Solution 1a: Compute noise ceilings

The first idea is to determine by how much our correlation estimate is biased. If we just knew this number, we should be able correct for it, no? To figure this out we can ask ourselves what the correlation between two measured activity patterns would be, if the true activity patterns were perfectly correlated. This is often called the *noise ceiling* for the correlation. 

To derive this quantity, we need to do a little bit of math. We assume that the measure patterns consist of the true pattern and measurement noise

$$
\begin{align}
\mathbf{y}_{a,i} = \mathbf{x}_{a} + \epsilon_{a,i}\\
\mathbf{y}_{b,i} = \mathbf{x}_{b} + \epsilon_{b,i}
\end{align}
$$

and that each of the terms has a specific variance (across voxels and repetitions): 

$$
\begin{align}
var(\mathbf{x}_a)=var(\mathbf{x}_b)=\sigma^2_{s}\\
var(\epsilon_a^2) = \sigma^2_{\epsilon a}\\
var(\epsilon_b^2) = \sigma^2_{\epsilon b}
\end{align}
$$

Then the correlation between the two tasks, assuming that their true patterns $\mathbf{x}_a$ and $\mathbf{x}_b$ are perfectly correlated, would be: 

$$
\begin{align}
r_{ceil}=\frac{cov(\mathbf{x}_a,\mathbf{x}_b)}{\sqrt{var(\mathbf{x}_a),var(\mathbf{x}_a)}}=\frac{\sigma^2_s}{\sqrt{(\sigma^2_s+\sigma^2_{\epsilon a})(\sigma^2_s+\sigma^2_{\epsilon b})}}
\end{align}
$$

Now - how can we estimate the variance of the true pattern and the measurement noise? If we have multiple measures of our pattern, we can estimate the split-half reliability, the correlation between two independent halves of the data. If we assume that the noise has the same variance across these two halves, the expected value of the split-half correlation is 

$$
r_{rel,a}=r(\mathbf{y}_{i,1},\mathbf{y}_{i,2})=\frac{cov(\mathbf{y}_{a,1},\mathbf{y}_{a,2})}{\sqrt{var(\mathbf{y}_{a,1}),var(\mathbf{y}_{a,2})}}=\frac{\sigma_s}{\sigma^2_s+\sigma^2_{\epsilon a}}.
$$

By substitution in the previous formula, we can see that the noise ceiling for a correlation between two measured vectors (ie. the value that we should get if the true vectors were perfectly correlated) is the *geometric mean*, i.e. the square-root of the product, of the two reliabilities.
{+margin: This is the noise ceiling for the correlation between each of the two independent halves of the data. If we are interested in the noise ceiling for the correlation between the mean measured patterns, we need to account for the fact that we averaged of 2 (or in general $N$) independent measure. See the accompanying jupyter notebook for details. }

$$
r_{ceil}=\sqrt{r_{rel,a} r_{rel,b}}
$$

So now we should just be able to normalize our measured correlation by dividing it by the noise ceiling for correlation. As can be seen in Figure 3 (solid blue line) this works quite well if the signal to noise ratio is high. In this case the corrected estimate approaches the true correlation. For low signal-to-noise levels (and with fMRI we are usually in this domain) the correction stops working correctly. What is going on? 

![Figure3](Figure_3.html)**Figure 3**. Mean correlation estimates for simulated data. Uncorrected (green line), corrected by noise ceiling (blue line), or correction by using cross-block covariances (red-line). 

One problem is that in some cases $r_{rel,a}$ or $r_{rel,b}$ (or both) become negative, so that a real square root does not exist anymore.  Here we have two options: Either we exclude these values from further analysis (solid line), or we replaced them with a specific value, for example $0$ (dashed line). Latter process is called *imputation*. Unfortunately, neither exclusion nor imputation fixes the problem. Both procedures show initially a positive bias, switching into a negative bias for very low signal to noise values. In general the problem is that the estimates become quite unstable when one of the reliabilities gets small. 

## Solution 1b: Use cross-partition covariances
A related solution is to use so-called "cross-validated" estimates of the correlation. Here, we calculate the correlation as usual, but estimate the variance and covariances of the patterns from the covariances across the  $N$ different independent measures of the patterns.   

$$
\begin{align}
\hat{cov}(\mathbf{x}_a,\mathbf{x}_b) = \frac{1}{N(N-1)}\sum_{i \neq j}cov(\mathbf{y}_{a,i},\mathbf{y}_{b,j})\\
\hat{var}(\mathbf{x}_a) = \frac{1}{N(N-1)}\sum_{i \neq j}cov(\mathbf{y}_{a,i},\mathbf{y}_{a,j})
\end{align}
$$

These unbiased estimators we then plug into our correlation formula:

$$
r_{cb}=\frac{\hat{cov}(\mathbf{x}_a,\mathbf{x}_b)}{\sqrt{\hat{var}(\mathbf{x}_a)\hat{var}(\mathbf{x}_a)}}.
$$

This correlation (Figure 3, red line) behaves very similar to the noise-ceiling corrected estimator. Indeed, if you dig a bit through the math, you will realize that they differ only in the sense that one uses the ratio of correlations, the other one of covariances. Again we have the problem that some of our variance estimator can become very small or negative, leading to unstable or missing correlation estimates.  

</section>

<section markdown="1">

## Solution 2: Using Pattern Component Modelling 
Ok, so what can we do instead? Obtaining unbiased estimates of the true correlation, is, as we have seen, very tricky. The best solution therefore is to turn the problem around: Rather than asking which correlation is the best estimate given the data, let's instead ask how likely the data is given different levels of correlation. We can do this by using the generative model shown in Figure 1 combined with the assumption of normal distributions for the true patterns and noise. Then we can calculate $p(Y|r)$, the probability of the data given a specific correlation $r$. The technical details of model fitting and evaluation are implemented in the [Pattern Component Modelling (PCM) toolbox](https://github.com/DiedrichsenLab/PcmPy), for which we have recently released a Python version. 

![Figure4](Figure_4.html)**Figure 4**. Simulation with $r = 0.7$ and a signal-to-noise of $0.5$. Light gray lines: Log-likelihood of 20 data data sets under correlation models between 0 and 1. Maximum likelihood estimates of the correlation are indicated by gray dots. Dark red line: Average log-likelihood and standard error. 

Figure 4 shows an example of this approach. The light gray lines indicate the log-likelihood ($log p(Y|r)$) of individual data sets given true correlations between 0 and 1. The gray dot on each line is the maximum-likelihood estimate of the true correlation, which we can obtain by fitting a model that has a free correlation parameter. While this estimate behaves a bit better than the noise-ceiling-corrected or cross-block estimates of the correlation, it still is not unbiased. For example, you could not test the hypothesis that the true correlation is 1. You would likely get a significant result even if the true correlation was 1, as tge estimates can be smaller, but not larger than this value. 

The rescue, however, is that we have the full likelihood curves for each participants. As you can see, some of these curves are very flat - indicates that the data is nearly equally likely under all correlations. This is the case where the measured patterns were not very reliable and hence give us little information about the true correlation. Some of the likelihood curves have a clear peak - these are cases with reliable activity patterns which provide more information. The maximum of the mean log-likelihood curve (red solid line) is therefore close to the true correlation of $0.7$. 

One way to test specific hypothesis is to use standand frequentist tests, using the log-likelihood as a dependent variable. For example, does the correlation model of $0.7$ fit the data better than a model that assume perfect correlation? When we conduct the paired t-test across the $20$ log-likelihood estimates, we find that $t(19)=0.029, p=0.97$ would not be significant. On the other hand, a correlation of $0.7$ would be significantly more likely than a correlation of $0.65$. 

Instead of using frequentist test, we can also use the likelihoods in a Bayesian group analysis{+side: for a good introduction, see [+citet:Stephan2009]}. If we assume that all correlations between $-1$ and $1$ are equally probable *a priori*, we can simply take the exponential of the log-liklihood and normalize the resulting probabilities to 1, giving us an approximate posterior distribution on the individual correlation. In this setting, a difference in log-likelihood of larger than $1$ is considered "worth talking about". 

## Technical considerations 
I hope at this point you can see the advantages of using a generative approach (as in PCM) to evaluate the correlations between activity patterns. Before jumping in and using the PCM toolbox, however, it is good to understand a few technical details that happen behind the scenes. 

To evaluate the likelihood of the data given a specific correlation, we need to deal with some additional parameters, in our case the variance of the signal ($\mathbf{x}_a$,$\mathbf{x}_b$),  and the noise ($\epsilon$). 
Let's denote these hyper-parameters {+side:These unknowns are considered hyper-parameters (rather than parameters), as they characterize the distribution of the patterns, rather than the patterns themselves}.
collectively by $\theta$. A practical way of dealing with them is to replace them using the maximum likelhood estimates. Thus, we would approximate our desired probability with

$$
p(Y|r) \approx max_{\theta}{p(Y|r,\theta)}.
$$

These may seem like a bit of a cheat, but works in this this case quite well. Estimating parameters on the same data that you use to evaluate the model of course leads to an overestimation of the likelihood. However, as the number of hyper-parameters is low and all correlation models have the same number of parameters, this bias will be approximately stable across all models. Since we are interested in the *difference* in log-likelihood across models, this small bias simply disappears. 

If you want to compare models with different numbers of parameters, a more sophisticaed approach is required. For example, in Figure 4, we may want to test whether the likelihood for the maximum likelihood estimate for the correlation is larger than the correlation for 1. If we simly take the maximum likelihood for each subjects, the answer would be yes. A slightly different approach would be to use the group-estimate of the best correlation. While this reduced the bias tremendously, it is still a bit biased, as the mean still contains the data from the subject on which we are testing. In this case, we should determine the best fittign correlation on 19 subject, and evalute the likelihood on the last remaining subject. For more on group fits and cross-validated group fits see the PCM documentation.{+margin:Another approach is to become even "more Bayesian" and treat the parameters as unkown variables with a prior, and then introduce "hyper-hyper parameters" to describe these priors [+citep:Friston2019]}.  

## Extensions
The situation considered here with two activity patterns and two measures per activity pattern is quite simple. In most experiments, we have more complicated situations. Often want to know the correlation between patterns associated with specific items observed under two conditions. For example, we want to know how the patterns associated with 4 different movements correlate (on average) across planning and execution. Or how the pattern associated with 30 objects correlated when they are presented as words or signs. In these cases we need to model the general differences between the 2 conditions (i.e planning vs. execution, or words vs. signs). Additionally, we often need to account for the correlation between patterns in an imaging run, or different co-variance between the patterns for different items. Coming up with a good solution for all these problems using the noise-ceiling or cross-block approach can be very difficult. I find it much easier to add these details into the generative model - and indeed all these situations are implemented in the PCM toolbox.  

## Three takehomes 

* Correlations estimated on noise data underestimate true correlations, making it difficult to test any hypothesis other than testing against zero. 
* Correction of the correlations using a noise ceiling (or using cross-validated correlations) provides valid answers when the signal-to-noise is high. However, when the signal-to-noise level is low, these approaches become biased and unstable. 
* Using the entire log-likelihood function across correlations of different size allows us to test specific hypothesis even if the signal-to-noise level is low. 

As you can see from the example in Figure 4, using a generative approach is not a magic bullet that suddenly gives you significant results from very noisy data. For example, we could not rule out that the correlation was anywhere between $0.7 - 1.0$. But at least if provides a valid (and in the Bayesian sense optimal) evaluation of the real evidence that you have in your data about the true correlation between two activity patterns. 
</section>
