# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 09:46:41 2018

@author: akansal2
"""
##############################################################
#importing libraries
import numpy as np



##############################################################
#input graph of connections between webpages
links = {
    'webpage-1': set(['webpage-2', 'webpage-4', 'webpage-5', 'webpage-6', 'webpage-8', 'webpage-9', 'webpage-10']),
    'webpage-2': set(['webpage-5', 'webpage-6']),
    'webpage-3': set(['webpage-10']),
    'webpage-4': set(['webpage-9']),
    'webpage-5': set(['webpage-2', 'webpage-4']),
    'webpage-6': set([]), # dangling page
    'webpage-7': set(['webpage-1', 'webpage-3', 'webpage-4']),
    'webpage-8': set(['webpage-1']),
    'webpage-9': set(['webpage-1', 'webpage-2', 'webpage-3', 'webpage-8', 'webpage-10']),
    'webpage-10': set(['webpage-2', 'webpage-3', 'webpage-8', 'webpage-9']),
}


###############################################################

#Objective is to rank all the webpages

################################################################
#step 1 - Initialize all the webpages by 1/n page rank(V matrix)

l = len(links.keys())
Initial_PR = 1/l

V = np.ones((l,1)) * Initial_PR



#########################################################################
#step 2 - Find the transition matrix value i.e probability of going to one node from other node

H = np.zeros((l,l))

#convert dict of webpages in form of numbers so that we can iterate thru it

mapping = {}
for counter,key in enumerate(links.keys()):
    mapping[key] = counter

# new dictionary with all integers
A = {}
    
#updating all values
for i,j in links.items():
    temp = []
    for item in j:
        temp.append(mapping[item])
    A[mapping[i]] = temp



#function to return the probablity of particular cell
def get_prob(i,j,l):
    out_nodes = int(len(A[j]))
    if out_nodes > 0:
        temp_prob = 1/out_nodes
        if i in A[j]:
            return temp_prob
        else:
            return 0
    else:
        #dangling node- Assign equal probablity of transitionning to all pages
        return 1/l
       

#creating transition matrix
for i in range(H.shape[0]):
    for j in range(H.shape[1]):
        H[i,j] = get_prob(i,j,l)

        


###############################################################################

#step3 - Multiple page rank matrix and transition matrix to get better page ranks


def get_newPageRank(epsilon,d,H,V):
    N = H.shape[0]
    temp = np.ones(N).reshape(N,1)*(1-d)/N   + d*np.matmul(H,V)
    
    if abs(V-temp).sum() > epsilon:
        V = temp
        temp = get_newPageRank(0.0001,0.85,H,temp)
    
    return V



#step 4 - Keep doing this untill the sum of(PR(prev)- PR(current)) < epsilon
V = get_newPageRank(0.0001,0.85,H,V)

#Step 5- Sort the webpages based on the ranks 

temp = sorted(list(V[:,0]),key = float,reverse = True)

final_list = []
for v in temp:
    for ind,value in enumerate(list(V[:,0])):
        if v== value:
            x = list(mapping.keys())[list(mapping.values()).index(ind)]
            if x not in final_list:
                final_list.append(x)
                break
            else:
                continue
            
    
#step 6 select the first 5 high rank webpages
top_rankers = 4
for i in range(top_rankers):
    print(final_list[i])























