'''
Function needed to be optimized for final evaluation
'''
import pandas as pd
import numpy as np

thresbig=1e6

def evaluation(beta,*ARGS):

    L=0.;   # Initial cost function
    season_id=ARGS[0] # season id
    rank_type=ARGS[1]
    epsilon=ARGS[2]
    losstype=ARGS[3]
    comparetype=ARGS[4]
    gamma=ARGS[5]

    df_rank=pd.read_csv('../WDataFiles/RegularSeasonCompactResults_'+str(season_id)+'_'+rank_type+'_'+comparetype+'_g'+str(gamma)+'.csv',sep=' ', header=None)
    
    if losstype=='train':df_data=pd.read_csv('../WDataFiles/RegularSeasonCompactResults_'+str(season_id)+'_'+comparetype+'.csv',sep=' ', header=None)
    elif losstype=='test':df_data=pd.read_csv('../WDataFiles/WNCAATourneyCompactResults_'+str(season_id)+'_'+comparetype+'.csv',sep=' ', header=None)

    rank= df_rank.set_index(0).to_dict()[1]

    M=len(df_data)

    for idx,rows in df_data.iterrows():

        Wteam=rows[0]
        Lteam=rows[1]

        p_ij=1./(epsilon+1.+np.exp(-2.*beta*(rank[Wteam]-rank[Lteam])))
        p_ij=push_to_extreme(p_ij,lmbd=0)

        L-=np.log(p_ij)
    
    print(-L/float(M),beta)

    outvalue=L/float(M)
    if outvalue>thresbig: raise SystemExit("Loss is bigger than admitted threshold: L = "+str(outvalue)+" > "+str(thresbig))

    return outvalue



def accuracy(season_id,rank_type,beta,comparetype,gamma):
    '''
    Count number of well predicted match outcomes
    '''
    acc=0.
    df_rank=pd.read_csv('../WDataFiles/RegularSeasonCompactResults_'+str(season_id)+'_'+rank_type+'_'+comparetype+'_g'+str(gamma)+'.csv',sep=' ', header=None)
    df_data=pd.read_csv('../WDataFiles/RegularSeasonCompactResults_'+str(season_id)+'_'+comparetype+'.csv',sep=' ', header=None)

    rank= df_rank.set_index(0).to_dict()[1]

    M=len(df_data)

    for idx,rows in df_data.iterrows():

        Wteam=rows[0]
        Lteam=rows[1]

        if rank[Wteam]>=rank[Lteam]:acc+=1
        
    return acc,M


def push_to_extreme(p_ij,lmbd=0,epsilon=0.001):
    '''
    Spinge verso gli estremi 0 ed 1 una predizione via di mezzo p_ij circa 0.5
    '''
    if lmbd==0:return p_ij
    # elif lmbd==0:
    #     if p_ij<0.5:return 0+epsilon
    #     else: return 1-epsilon
    else:
        return (np.tanh(p_ij*lmbd-0.5*lmbd)+1)/2.+epsilon
