# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 16:18:02 2018

@author: akansal2
"""
#####################################importing libraries
import re
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag



########################## getting input file and converting it into list of statements


text = []
file = open(r'''C:\A_stuff\News.txt''')

for line in file.readlines():
    text.append(line)

file.close()    
text = re.split(r'\.',text[0])
text = list(filter(None,text))


text = ['Cow has 4 legs',
        'Cow has one tail',
        'Cow is a good animal',
        'Buffolo is same species as Cow',
        'I like cow'
        
        ]

###################################################

    
def perform_operation(a,b):
    a = Lemmatizewords(a)
    b = Lemmatizewords(b)
    cv = TfidfVectorizer(stop_words = 'english')
    sparse_matrix = cv.fit_transform([a,b]).toarray()
    score = Cosine_Similarity(sparse_matrix[0],sparse_matrix[1])
    return score

   
def Lemmatizewords(a):
    a = str(a)
    a = re.sub(r'[^\w]',' ',a )
    a = a.split(' ')
    a = list(filter(None,a))   
    temp = []
    for i in a:
        i = i.lower()
        lem = WordNetLemmatizer()
        word = word_tokenize(i)
        pos1 = pos_tag(word)
        #print(pos1)
        if pos1[0][1] == 'RBR':
            temp.append(lem.lemmatize(i,pos ='a')) 
        elif pos1[0][1] == 'VBG':
            temp.append(lem.lemmatize(i,pos ='v'))
        else:
            temp.append(lem.lemmatize(i,pos ='n'))
                        
    a = ' '.join(temp)  
    return a
      
    
def Cosine_Similarity(X,Y):
    dot_product = np.dot(X,Y)
    norm_X = np.linalg.norm(X)
    norm_Y = np.linalg.norm(Y)
    return dot_product/(norm_X*norm_Y)


#############################################################################
#step 1 - Initialize all the sentences by 1/n page rank(V matrix)

l = len(text)
Initial_PR = 1/l

V = np.ones((l,1)) * Initial_PR



#########################################################################
#step 2 - Find the transition matrix value i.e probability of going to one node from other node

H = np.zeros((l,l))


#creating transition matrix
for i in range(H.shape[0]):
    for j in range(H.shape[1]):
        if i == j:
            continue
        else:
            H[i,j] = perform_operation(text[i],text[j])
            

        


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
            x = text[ind]
            if x not in final_list:
                final_list.append(x)
                break
            else:
                continue
            
    
#step 6 select the first 5 high rank webpages
top_rankers = 4
for i in range(top_rankers):
    print(final_list[i])
































