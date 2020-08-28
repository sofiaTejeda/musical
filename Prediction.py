import numpy as np
import pandas as pd
import math
import random
import sklearn
import scipy
import clases as cs

from sklearn.model_selection import cross_validate as cv 
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics.pairwise import cosine_similarity
import scipy.sparse as sp
from scipy.sparse.linalg import svds
from surprise import KNNBasic,KNNWithMeans
from surprise import SVD



class BasePrediction:

    def __init__(self,train,test):
        self.Train = train
        self.Test=test
        print("base pred")

    def SvdAlgorithmFunc(self,kk):

        model = SVD(n_factors=kk)
        model.fit(self.Train)
        return model  

   
    
    def CalcularMatrizSimilaridad(self):
        sim_options = {'name': 'cosine',
               'user_based': True, 'min_support' : 1 
               }
        model = KNNBasic(sim_options=sim_options)
        model.fit(self.Train)
        simMatrix=model.sim
        return model, simMatrix

    
    def CosineAlgorithm(self):
        cosine = cosine_similarity(self.R)
        np.fill_diagonal(cosine, 0 )
        b = cosine_similarity(self.R)
        np.fill_diagonal(b, 0 )
        similarity_with_user = pd.DataFrame(b,index=self.R.index)
        similarity_with_user.columns=self.R.index
        pred=self.predictcosinealgorithm(self.R,similarity_with_user)
        return pred
    
    def CosineAlgorithmSurprise(self):
        sim_options = {'name': 'cosine',
               'user_based': True, 'min_support' : 1 
               }
        model = KNNBasic(sim_options=sim_options)
        model.fit(self.Train)
        #testset = self.Train.build_anti_testset()
        #predictions = model.test(testset)
        predictions = model.test(self.Test)

        df = pd.DataFrame(predictions, columns=['user_id', 'song_id', 'listen_count', 'prediction','details'])    
        return model,df

    def SVDAlgorithmPredict(self,k):       
        model = SVD(n_factors=k)
        model.fit(self.Train)
        predictions = model.test(self.Test)
        df = pd.DataFrame(predictions, columns=['user_id', 'song_id', 'listen_count', 'prediction','details'])    
        return model,df


    def CosineAlgorithmPredict(self,model):
        predictions = model.test(self.Test)
        df = pd.DataFrame(predictions, columns=['user_id', 'song_id', 'listen_count', 'prediction','details'])    
        return df


    def predictcosinealgorithm(self,ratings,similarity):
        usertest=[]
        mean_user_rating = ratings.mean(axis=1)
        ratings_diff = (ratings - mean_user_rating[:, np.newaxis])
        dotrepsimilarity=similarity.values.dot(ratings_diff) 
        sumsimilarity=np.array([np.abs(similarity).sum(axis=1)]).T
        i=0
        for index, row in similarity.iterrows():
            predbyuser=mean_user_rating.loc[mean_user_rating.index==index]
            ratinguser=ratings_diff.loc[ratings_diff.index==index]
            mean=predbyuser[0]
            corr=dotrepsimilarity[i]
            sums=sumsimilarity[i]
            i=i+1
            newuser=cs.UsuarioCoseno(index,row,mean,ratinguser,corr,sums)        
            usertest.append(newuser) 
        return usertest

        


