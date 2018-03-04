'''
Example of SPringRank usage

From a given seasonID, it extracts the SpringRank scores

'''

from __future__ import print_function
import networkx as nx
import numpy as np
import SpringRank_tools as sr
import tools as tl


alpha=0.
l0=1.
l1=1
season=list(np.arange(1998,2018))


for comparetype in ['min','max','sum','vic']:


	for seasonID in season:

		inadjacency='../WDataFiles/WRegularSeasonCompactResults_'+str(seasonID)+'_'+str(comparetype)+'.csv'

		G=tl.build_graph_from_adjacency(inadjacency)

		nodes=list(G.nodes())			#  determines the order of the entries of matrix A

		A=nx.to_numpy_matrix(G,nodelist=nodes)


		'''
		Extracts SpringRank
		'''
		rank=sr.SpringRank(A,alpha=alpha,l0=l0,l1=l1)

		rank=tl.shift_rank(rank)   # shifts so that the min is in zero and the others are positive

		'''
		Order results so that the first node is the highest-ranked one
		'''
		X=[(nodes[i],rank[i]) for i in range(G.number_of_nodes())]
		X= sorted(X, key=lambda tup: tup[1],reverse=True)
		'''
		Prints results
		'''
		print('SpringRank scores:')
		outfile='../WDataFiles/WRegularSeasonCompactResults_'+str(seasonID)+'_SpringRank_'+str(comparetype)+'.csv'
		outf=open(outfile,'w')

		for i in range(G.number_of_nodes()):
			print(X[i][0],X[i][1],file=outf)
			# print(nodes[i],rank[i])
			print(X[i][0],X[i][1])
		print("");	
		print('Results saved in:',outfile)
		outf.close()
