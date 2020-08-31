import MainEval as maineval2
import Recommender as rc
import clases as cs
import BuildGraph as bg
from surprise import SVD
from surprise import accuracy
from surprise.model_selection import train_test_split
from surprise import Reader, Dataset
import pandas as pd
from surprise import KNNBasic
from heapq import nlargest
import heapq
import random
import numpy
import AnalisisAlgoritmoRecomendacion as an
from surprise import accuracy

#Probar Performance
"""
an.EscuchaDadoPorUsuarios()
an.GraphPerformances()
"""
#Recomendar Cancion
"""df=rc.Recommender(1000,60)
recomendacion=df.EvalAlgorithm(10,"a820d2d4f16bbd53be9e41e0417dfb234bfdfba8")
print("Cancion Recomendada")
for c in recomendacion.CancionRecomendada:
    print("Cancion: "+c.Nombre+ " Autor:"+ c.ArtistName+" score: "+str(c.ListenCount))

print("cancione escuchada")
for c in recomendacion.CancionEscuchada:
    print("Cancion: "+c.Nombre+ " Autor:"+ c.ArtistName+" score: "+str(c.ListenCount))
"""

#DIVIDIR DATA EN TRAIN Y TEST
"""DIVIDIR DATA EN TRAIN Y TEST
UserRating= pd.read_csv(r'traindata.csv')
testdata=pd.read_csv(r'testdata.csv')
test=testdata.values.tolist()
dictmusicprepared= {
'song_id': (UserRating.song_id),
'user_id': list(UserRating.user_id),
'rating': list(UserRating.listen_count)}
reader= Reader(rating_scale=(1, 100))
dftrain=pd.DataFrame(dictmusicprepared)
DataMusicTrain=Dataset.load_from_df(dftrain[['user_id', 'song_id', 'rating']], reader)
trainsetfull = DataMusicTrain.build_full_trainset()
model = SVD(n_factors=60)
model.fit(trainsetfull)
predictions = model.test(test)
r=accuracy.rmse(predictions)
print(r)
df = pd.DataFrame(predictions, columns=['uid', 'iid', 'rui', 'est', 'details'])

df['err'] = abs(df.est - df.rui)
best_predictions = df.sort_values(by='err')[:10]
print(best_predictions)
"""
#Guardar Mil Usuarios

"""
mn=maineval2.Main()
mn.LoadDataEval()
users= mn.UserRating[['user_id']]
users=users.drop_duplicates()
users = users.sample(frac = 1)
users=users.head(1000)
mn.UserRating=mn.UserRating[mn.UserRating['user_id'].isin(users['user_id'].tolist())]
dataframf=pd.DataFrame(mn.UserRating, columns=['user_id', 'song_id','listen_count','title','release','artist_name','year'])
dataframf.to_csv('subset2.csv')
"""
#TEST AND TRAIN
"""TestDataUse=pd.DataFrame(test_data.copy(), columns=['user_id', 'song_id','listen_count'])
usertrain=train._raw2inner_id_users
listuser=[]
df1 = pd.DataFrame(usertrain.keys()) 
df1=df1[df1.columns[0]].unique()
datatrain=[]
for i in df1:
    data=mn.UserRating[mn.UserRating.user_id==i]   
    datatest=TestDataUse[TestDataUse.user_id==i]
    songid=datatest["song_id"]
    songid=songid.unique()
    for index,row in data.iterrows():
        if (row["song_id"] not in songid):
            datatrain.append(row)

dataframf=pd.DataFrame(datatrain, columns=['user_id', 'song_id','listen_count'])

TestDataUse.to_csv('testdata.csv')
dataframf.to_csv('traindata.csv')
mn.UserRating.to_csv("userating.csv")
#lstresult=mn.EvalCosineAlgorithm()
""" 

#an.EscuchaDadoPorUsuarios()
"""df=rc.Recommender(1000,60)
recomendacion=df.EvalAlgorithm(10,"a820d2d4f16bbd53be9e41e0417dfb234bfdfba8")
print("Cancion Recomendada")
for c in recomendacion.CancionRecomendada:
    print("Cancion: "+c.Nombre+ " Autor:"+ c.ArtistName+" score: "+str(c.ListenCount))

print("cancione escuchada")
for c in recomendacion.CancionEscuchada:
    print("Cancion: "+c.Nombre+ " Autor:"+ c.ArtistName+" score: "+str(c.ListenCount))
"""
#Crear Grupos
"""df=rc.Recommender(1000,60)
recomendacion=df.CreateGrupo()
"""



