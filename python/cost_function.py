'''
Function needed to be optimized for final evaluation
'''

def evaluation(beta,*ARGS):

    L=0.;   # Initial cost function
    season_id=ARGS[0] # season id
    rank_type=ARGS[1]
    
   	df_rank=pd.read_csv('../WDataFiles/WRegularSeasonCompactResults_'+str(season_id)+'_'+rank_type+'.dat',sep=' ', header=None)
   	df_data=pd.read_csv('../WDataFiles/WRegularSeasonCompactResults_'+str(season_id)+'_adjacency.csv',sep=' ', header=None)

   	rank= df_rank.set_index(0).to_dict()[1]

   	M=len(df_data)

    for idx,rows in df_data.iterrows():

		Wteam=rows[0]
		Lteam=rows[1]

		p_ij=1./(1.+exp(-2.*beta*(rank[Wteam]-rank[Lteam])))

		L-=np.log(p_ij)

    return -L/float(M)



def accuracy(season_id,rank_type,beta):
	'''
	Count number of well predicted match outcomes
	'''
	acc=0.
	df_rank=pd.read_csv('../WDataFiles/WRegularSeasonCompactResults_'+str(season_id)+'_'+rank_type+'.dat',sep=' ', header=None)
   	df_data=pd.read_csv('../WDataFiles/WRegularSeasonCompactResults_'+str(season_id)+'_adjacency.csv',sep=' ', header=None)

   	rank= df_rank.set_index(0).to_dict()[1]

   	M=len(df_data)

    for idx,rows in df_data.iterrows():

		Wteam=rows[0]
		Lteam=rows[1]

		if rank[Wteam]>=rank[Lteam]:acc+=1
		
    return acc,M