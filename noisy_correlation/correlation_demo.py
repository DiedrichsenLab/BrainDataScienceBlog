import numpy as np 
import PcmPy as pcm
from PcmPy import sim
import pandas as pd
import plotly.express as pe 
import plotly.io as pio 
import plotly.graph_objects as go

def get_corr(X,cond_vec):
    p1 = X[cond_vec==0,:].mean(axis=0)
    p2 = X[cond_vec==1,:].mean(axis=0)
    return np.corrcoef(p1,p2)[0,1]

def get_noiseceil(X,cond_vec):
    rel = np.array([0.0,0.0])
    for i in [0,1]: 
        N = np.sum(cond_vec==i) # Number of measurements  
        R = np.corrcoef(X[cond_vec==i,:]) # Correlation matrix 
        index_R = np.where(~np.eye(N,dtype=bool)) # Average cross-block correlations 
        r = np.mean(R[index_R]) # Average the non-diagnal elements. 
        rel[i] = r * N / (r*(N-1)+1) # Overall realibility of the mean 

    # Check if both are above zero
    if rel[0]>0 and rel[1]>0:
        noise_r = np.sqrt(rel[0]*rel[1])
    else: 
        noise_r = np.nan 
    return noise_r 

def do_sim(corr,signal=np.linspace(0,5,20),n_sim=50): 
    M = pcm.CorrelationModel('corr',num_items=1,corr=corr,cond_effect=False)
    G,dG = M.predict([0,0])
    cond_vec,part_vec = pcm.sim.make_design(2,2)
    Lcorr = []
    LnoiseCeil = [] 
    Lsign = []
    for s in signal:
        D = pcm.sim.make_dataset(M, [0,-0.5], cond_vec, n_sim=n_sim, signal=s)
        for i in range(n_sim):
            data = D[i].measurements
            Lcorr.append(get_corr(data,cond_vec))
            LnoiseCeil.append(get_noiseceil(data,cond_vec))
            Lsign.append(s)
    S = pd.DataFrame({'r_naive':Lcorr,'signal':Lsign,'noiseCeil':LnoiseCeil})
    return S


if __name__ == "__main__":
    D = do_sim(1,n_sim=50)
    D['noiseceil_nan'] = np.isnan(D.noiseCeil)
    D['corr_corrected'] = D.r_naive / D.noiseCeil
    T = D.groupby("signal").apply(np.mean)
    Tstd = D.groupby("signal").apply(np.std)
    pass