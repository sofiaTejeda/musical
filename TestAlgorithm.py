import MainEval
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

#performance
#an.EscuchaDadoPorUsuarios()
#an.GraphPerformances()
#Recomendar Cancion
df=rc.Recommender(1000,60)
recomendacion=df.EvalAlgorithm(10,"9bb911319fbc04f01755814cb5edb21df3d1a336")
print("Cancion Recomendada")
for c in recomendacion.CancionRecomendada:
    print("Cancion: "+c.Nombre+ " Autor:"+ c.ArtistName+" score: "+str(c.ListenCount))

print("cancione escuchada")
for c in recomendacion.CancionEscuchada:
    print("Cancion: "+c.Nombre+ " Autor:"+ c.ArtistName+" score: "+str(c.ListenCount))

#creargrhpos
#df=rc.Recommender(1000,60)
#recomendacion=df.CreateGrupo()


"""

#df.CreateGrupo() 11
#an.EscuchaDadoPorUsuarios()
#an.GraphPerformances()
"""
"""
CREAR GRUPOS
mn=maineval2.Main2()
mn.LoadDataRecomender()
mn.PreprocessDataPredictor()
usergroups=mn.CreateGroupsWithSimilaritiesFunc()
for g in usergroups:
    print(g.Identificador)
    for u in g.Usuarios:
        print(u.UsuarioId)

mn=maineval2.Main2()
mn.LoadDataRecomender()
mn.PreprocessDataPredictor()
usertrain=mn.FinalRatingSVD._raw2inner_id_users
traindata=mn.FinalRatingSVD
sim_options = {'name': 'cosine',
'user_based': True, 'min_support' : 1 
}
model = KNNBasic(sim_options=sim_options)
model.fit(traindata)
simMatrix=model.sim
listuser=[]
df1 = pd.DataFrame(usertrain.keys()) 
df1=df1[df1.columns[0]].unique()
usergroups= [] 
m=1
k=1
while (len(df1) > 0):
    userlist=[]
    userlstid=[]       
    n = random.randint(4,9)
    user=df1[0]            
    testuserInnerId=traindata.to_inner_uid(user)
    similarUsers=[]
    similarityrow=simMatrix[testuserInnerId]
    df1 = df1[df1!= user]
    for innerid,score in enumerate(similarityrow):
        if(innerid!=testuserInnerId):
            usersimilarid=traindata.to_raw_uid(innerid)
            if usersimilarid in df1:
                similarUsers.append((usersimilarid,score))
    Kneighbors=heapq.nlargest(n,similarUsers,key=lambda t: t[1])
    userlstid.append(user)
    for similaruser in Kneighbors: 
        innerid=similaruser[0]
        df1 = df1[df1!= innerid]
        userlstid.append(innerid)
    for i in userlstid:             
        newuser=cs.UsuarioArmarGrupo(i,0)
        userlist.append(newuser)
    newgroup=cs.GrupoUsuario(userlist,[])
    newgroup.Identificador="g"+str(m)
    if(len(userlist)>1):
        usergroups.append(newgroup)
        m=m+1

for g in usergroups:
    print(g.Identificador)
    for u in g.Usuarios:
        print(u.UsuarioId) 

mn=maineval2.Main2()
mn.LoadDataEval()
mn.PreprocessData(1000)
lstresult=mn.EvalCosineAlgorithm()
for i in lstresult:
    print(i.Descripcion+": "+str(i.Valor))

lstresultsvd=mn.EvalSvdAlgorithm(60)
for i in lstresult:
    print(i.Descripcion+": "+str(i.Valor))

mn=maineval2.Main2()
mn.LoadDataEval()
users= mn.UserRating[['user_id']]
users=users.drop_duplicates()
users = users.sample(frac = 1)
users=users.head(1000)
userid=users.head(1)
userid=userid["user_id"]
mn.UserRating=mn.UserRating[mn.UserRating['user_id']
.isin(users['user_id'].tolist())]

dictmusicprepared= {
        'song_id': (mn.UserRating.song_id),
        'user_id': list(mn.UserRating.user_id),
        'rating': list(mn.UserRating.listen_count)}
reader= Reader(rating_scale=(1, 100))
dftrain=pd.DataFrame(dictmusicprepared)
datatrain= Dataset.load_from_df(dftrain[['user_id', 'song_id', 'rating']], reader)
train_data, test_data = train_test_split(datatrain, test_size=.20) 
usertrain=train_data._raw2inner_id_users
listuser=[]
df1 = pd.DataFrame(usertrain.keys()) 
df1=df1[df1.columns[0]].unique()
print("total usuarios train: "+str(len(df1)))

sim_options = {'name': 'cosine',
               'user_based': True, 'min_support' : 1 
               }
model = KNNBasic(sim_options=sim_options)
model.fit(train_data)
simMatrix=model.compute_similarities()
usergroups= [] 
TestDataUse=pd.DataFrame(test_data, columns=['user_id', 'song_id','rating'])
test_searcheable= TestDataUse.set_index('user_id')
m=1
while (len(df1) > 0):
    userlist=[]
    cancionrecomendar=[]
    n = random.randint(2,5)
    listcanciones=[]
    for x in range(0,n):
        usercancionid=[]
        cancionusuario=[]
        if len(df1) > 0:
            user=df1[0]            
            df1 = df1[df1!= user]
            user_data = test_searcheable[test_searcheable.index == (user)]
            if len(user_data)>0:
                user_data=user_data["song_id"]
                for uc in user_data:
                    usercancionid.append(str(uc)) 
                    newcancion=cs.Cancion(uc,"title",0)  
                    cancionusuario.append(newcancion)
            listcanciones.append(usercancionid)
            newuser=cs.UsuarioArmarGrupo(user,len(user_data))
            newuser.CancionRecomendar=cancionusuario
            userlist.append(newuser)
            
    listcancionrecomendar=[]
    listcancionrecomendar = set(listcanciones[0])
    cancionesgrupo=[]
    for s in listcanciones[1:]:
        listcancionrecomendar.intersection_update(s)
    if(listcancionrecomendar!=set()):
        for i in listcancionrecomendar:
            print("cancion comun:" +i)
            newcancion=cs.Cancion(i,"title",0)
            cancionesgrupo.append(newcancion)
        for  u in userlist:
            u.CancionRecomendar=cancionesgrupo
        newgroup=cs.GrupoUsuario(userlist,cancionesgrupo)
        newgroup.Identificador="g"+str(m)
        if(len(userlist)>1):
            usergroups.append(newgroup)
            m=m+1
        
    else:
        listcancionrecomendar=[]        
        for  u in userlist:
            for c in u.CancionRecomendar:
                listcancionrecomendar.append(c.SongId)
        listcancionrecomendar=list(set(listcancionrecomendar))
        for i in listcancionrecomendar:
            newcancion=cs.Cancion(i,"title",0)
            cancionesgrupo.append(newcancion)
        newgroup=cs.GrupoUsuario(userlist,cancionesgrupo)
        newgroup.Identificador="g"+str(m)
        if(len(userlist)>1):
            usergroups.append(newgroup)
            m=m+1
while (len(df1) > 0):
    userlist=[]
    userlstid=[]
    cancionrecomendar=[]
    n = random.randint(4,9)
    user=df1[0]
    dictcanciones = {}            
    testuserInnerId=train_data.to_inner_uid(user)
    similarUsers=[]
    similarityrow=simMatrix[testuserInnerId]
    df1 = df1[df1!= user]
    for innerid,score in enumerate(similarityrow):
        if(innerid!=testuserInnerId):
            usersimilarid=train_data.to_raw_uid(innerid)
            if usersimilarid in df1:
                similarUsers.append((usersimilarid,score))
    Kneighbors=heapq.nlargest(n,similarUsers,key=lambda t: t[1])
    userlstid.append(user)
    for similaruser in Kneighbors: 
        innerid=similaruser[0]
        df1 = df1[df1!= innerid]
        userid=train_data.to_inner_uid(user)
        userlstid.append(innerid)
    cancionprohibida=[]
    for i in userlstid:
        userInnerId=train_data.to_inner_uid(i)
        trainset=train_data.ur[userInnerId]
        for s in trainset:
            innerid=s[0]
            c=train_data.to_raw_iid(innerid)
            cancionprohibida.append(c)
     

    for i in userlstid:
        user_data = test_searcheable[test_searcheable.index == (i)]
        user_data=user_data["song_id"]
        cancionusuario=[]
        for uc in user_data:
            if(uc not in cancionprohibida):
                newcancion=cs.Cancion(uc,"title",0)  
                cancionusuario.append(newcancion)
                if(uc in dictcanciones):
                    dictcanciones[uc] = dictcanciones[uc]+1
                else:
                    dictcanciones[uc]=1
 
        newuser=cs.UsuarioArmarGrupo(i,len(user_data))
        newuser.CancionRecomendar=cancionusuario
        userlist.append(newuser)
        
    listcancionrecomendar=[]
    for (key, value) in dictcanciones.items():
        if(value>1):
            listcancionrecomendar.append(key)
    cancionesgrupo=[]
    if(listcancionrecomendar!=[]):
        for i in listcancionrecomendar:
            newcancion=cs.Cancion(i,"title",0)
            cancionesgrupo.append(newcancion)
        for  u in userlist:
            u.CancionRecomendar=cancionesgrupo
        newgroup=cs.GrupoUsuario(userlist,cancionesgrupo)
        newgroup.Identificador="g"+str(m)
        if(len(userlist)>1):
            usergroups.append(newgroup)
            m=m+1
        
    else:
        listcancionrecomendar=[]        
        for  u in userlist:
            for c in u.CancionRecomendar:
                listcancionrecomendar.append(c.SongId)
        listcancionrecomendar=list(set(listcancionrecomendar))
        for i in listcancionrecomendar:
            newcancion=cs.Cancion(i,"title",0)
            cancionesgrupo.append(newcancion)
        newgroup=cs.GrupoUsuario(userlist,cancionesgrupo)
        newgroup.Identificador="g"+str(m)
        if(len(userlist)>1):
            usergroups.append(newgroup)
            m=m+1

totaluser=0
for i in usergroups:
    print(i.Identificador)
    print(i.Canciones)
    for j in i.Usuarios:
        totaluser=totaluser+1    
print(totaluser)

#_raw2inner_id_users
#rmsecos=mn.EvalCosineAlgorithm()
#print("rmse cosine "+str(rmsecos))

grupos=df.GetGrupos()
lastgroup=grupos[-1]
        
print(lastgroup)
usuarios=[]
for u in lastgroup.users:
    usuarios.append(u.id)

print(usuarios)
usuarioingroup=[]
for g in grupos
    for u in g.users:
        usuarioingroup.append(u.id)

newgroup=cs.GrupoUsuario(usuarios,[])
lstusuarios=bg.ArmarUsuario(usuarios,mn.UserRating)
"""

#mn=MainEval.Main(50)
#mn.PreprocessDataPredictor()
#rmsecos=mn.EvalCosineAlgorithm()
#print("rmse cosine "+str(rmsecos))


#rmsesvd=mn.EvalSvdAlgorithm()
#print("rmse SVD "+str(rmsesvd))
"""def EvalAlgorithm():
    mn=MainEval.Main()
    mn.LoadDataEval();
    mn.TransformData(10) 
  # rmsecos=mn.EvalCosineAlgorithm()
   #rmsesvd=mn.EvalSvdAlgorithm()
   #print("RMSE COSENO: "+rmsecos)
   #print("RMSE SVD: "+rmsesvd)
def recommendereval():
    df=rc.Recommender(20,6000,50)
    canciones=df.EvalAlgorithm(10,"f699589580393fdfe477a608ecc6aac3676cdd52")
    for c in canciones:
        print("Cancion: "+c.Nombre+ " Autor:"+ c.ArtistName+" score: "+str(c.ListenCount))"""