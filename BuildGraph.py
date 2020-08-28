import clases as cs
import numpy as np
import pandas as pd
import math
import random
import sklearn
import scipy
from heapq import nlargest
import heapq
import clases as cs


def RecommendSongsEvalAlgorithm(user,predictions,model):
    cancion=[]
    cancionrecomendar=[]
    for c in user.CancionRecomendar:
        result =predictions[predictions['song_id']==c.SongId]
        resp= next((l for l in user.Canciones if l.SongId==c.SongId), None)
        if(len(result.values)>0):
            cnscoren=cs.Cancion(c.SongId,"title",result["listen_count"].values.flat[0])
            cnscoren.SongPred=result["prediction"].values.flat[0]
            cancionrecomendar.append(cnscoren)
            if(resp!=None):
                canew=cs.Cancion(c.SongId,"title",result["listen_count"].values.flat[0])
                canew.ListenCount=result["listen_count"].values.flat[0]
                cancion.append(canew)    
        else:
            result=model.predict(user.UsuarioId, iid = c.SongId)
            cnscoren=cs.Cancion(c.SongId,"title",result.est)
            cnscoren.SongPred=result.est
            cancionrecomendar.append(cnscoren)
    user.CancionRecomendar=cancionrecomendar
    user.Canciones=cancion

def ArmarGruposDefAleatorioEval(df1,songs,traindata,datarating):
    usergroups= [] 
    a = []
    test_searcheable= datarating.set_index('user_id')
    m=1
    totalcomun=0
    while (len(df1) > 0):
        userlist=[]
        cancionrecomendar=[]
        n = random.randint(5,10)
        listcanciones=[]
        dictcanciones = {}            
        userlistid=[]
        cancionprohibida=[]
        for x in range(0,n):
            if len(df1) > 0:
                user=df1[0]            
                df1 = df1[df1!= user]
                userlistid.append(user)
                userInnerId=traindata.to_inner_uid(user)
                trainset=traindata.ur[userInnerId]
                for s in trainset:
                    innerid=s[0]
                    c=traindata.to_raw_iid(innerid)
                    cancionprohibida.append(c)
                
        for x in userlistid:
        
            usuariocancionlst=[]
            cancionusuario=[]
            if  1 > 0:
                user=x         
                user_data = test_searcheable[test_searcheable.index == (user)]
                if len(user_data)>0:
                    user_data=user_data["song_id"]
                    for uc in user_data:
                        if(uc not in cancionprohibida):
                            newcancion=cs.Cancion(uc,"title",0)  
                            cancionusuario.append(newcancion)
                            usuariocancionlst.append(uc)
                        """if(uc in dictcanciones):
                            dictcanciones[uc] = dictcanciones[uc]+1
                        else:
                            dictcanciones[uc]=1"""
         
                newuser=cs.UsuarioArmarGrupo(user,len(user_data))
                newuser.Canciones=cancionusuario
                listcanciones.append(usuariocancionlst)
                userlist.append(newuser)
        listcancionrecomendar=[]
        cancionesgrupo=[]

        listcancionrecomendar = set(listcanciones[0])
        for s in listcanciones[1:]:
            listcancionrecomendar.intersection_update(s)
    
        if(listcancionrecomendar!=set()):
            for i in listcancionrecomendar:
                
                newcancion=cs.Cancion(i,"title",0)
                cancionesgrupo.append(newcancion)
            for  u in userlist:
                u.CancionRecomendar=cancionesgrupo
                u.Canciones=cancionesgrupo
            newgroup=cs.GrupoUsuario(userlist,cancionesgrupo)
            newgroup.Identificador="g"+str(m)
            if(len(userlist)>1):
                usergroups.append(newgroup)
                m=m+1
        else:
            listcancionrecomendar=[]        
            for  u in userlist:
                for c in u.Canciones:
                    listcancionrecomendar.append(c.SongId)
            listcancionrecomendar=list(set(listcancionrecomendar))
            for i in listcancionrecomendar:
                newcancion=cs.Cancion(i,"title",0)
                cancionesgrupo.append(newcancion)
            for u in userlist:
                u.CancionRecomendar=cancionesgrupo
            newgroup=cs.GrupoUsuario(userlist,cancionesgrupo)
            newgroup.Identificador="g"+str(m)            
            if(len(userlist)>1):
                usergroups.append(newgroup)
                m=m+1
   
    return usergroups

def ArmarGruposDefSimilaresEval(df1,songs,traindata,datarating,simMatrix):
    usergroups= [] 
    test_searcheable= datarating.set_index('user_id')
    m=1
    k=1
    while (len(df1) > 0):
        userlist=[]
        userlstid=[]
        cancionrecomendar=[]
        dictcanciones = {}   
        listcanciones=[]       
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
        cancionprohibida=[]
        for i in userlstid:
            userInnerId=traindata.to_inner_uid(i)
            trainset=traindata.ur[userInnerId]
            for s in trainset:
                innerid=s[0]
                c=traindata.to_raw_iid(innerid)
                cancionprohibida.append(c)
            
        for i in userlstid:
            user_data = test_searcheable[test_searcheable.index == (i)]
            user_data=user_data["song_id"]
            usuariocancionlst=[]
            cancionusuario=[]
            for uc in user_data:
                if(uc not in cancionprohibida):
                    newcancion=cs.Cancion(uc,"title",0)  
                    cancionusuario.append(newcancion)
                    usuariocancionlst.append(uc)
                    """if(uc in dictcanciones):
                        dictcanciones[uc] = dictcanciones[uc]+1
                    else:
                        dictcanciones[uc]=1"""
         
            newuser=cs.UsuarioArmarGrupo(i,len(user_data))
            newuser.Canciones=cancionusuario
            listcanciones.append(usuariocancionlst)
            userlist.append(newuser)
            
        listcancionrecomendar=[]
        listcancionrecomendar = set(listcanciones[0])
        for s in listcanciones[1:]:
            listcancionrecomendar.intersection_update(s)
    
        #listcancionrecomendar=set.intersection(listcanciones)
        """lenuser=len(userlist)
        for (key, value) in dictcanciones.items():
            if(value>=lenuser):
                listcancionrecomendar.append(key)"""
        cancionesgrupo=[]
        if(listcancionrecomendar!=set()):
            
            for i in listcancionrecomendar:
                
                newcancion=cs.Cancion(i,"title",0)
                cancionesgrupo.append(newcancion)
            for  u in userlist:
                u.CancionRecomendar=cancionesgrupo
                u.Canciones=cancionesgrupo
            newgroup=cs.GrupoUsuario(userlist,cancionesgrupo)
            newgroup.Identificador="g"+str(m)
            if(len(userlist)>1):
                usergroups.append(newgroup)
                m=m+1
        
        else:
            listcancionrecomendar=[]        
            for  u in userlist:
                for c in u.Canciones:
                    listcancionrecomendar.append(c.SongId)
            listcancionrecomendar=list(set(listcancionrecomendar))
            for i in listcancionrecomendar:
                newcancion=cs.Cancion(i,"title",0)
                cancionesgrupo.append(newcancion)
            for u in userlist:
                u.CancionRecomendar=cancionesgrupo

            newgroup=cs.GrupoUsuario(userlist,cancionesgrupo)
            newgroup.Identificador="g"+str(m)
            if(len(userlist)>1):
                usergroups.append(newgroup)
                m=m+1

    return usergroups

def ArmarGruposDefSimilaresFunc(df1,traindata,simMatrix):
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


    return usergroups

def RecommendNumSongs(model, userid, songs, numrecommend):
    
    cancionusuario=[]
    for index, row in songs.iterrows():
        
        songid=(row["song_id"])
        result=model.predict(userid, iid = songid)
        cancion = cs.Cancion(row["song_id"], str(row["title"]),result.est)
        cancion.ArtistName=str(row["artist_name"])
        cancion.Release=str(row["release"])
        cancion.Year=row["year"]
        cancion.SongPred=result.est
        cancionusuario.append(cancion) 

    cancionusuario=sorted(cancionusuario, key=lambda cancionuser: cancionuser.ListenCount,reverse=True)
    cancionusuario=cancionusuario[:numrecommend] 
    newuser=cs.Usuario(userid,cancionusuario)    
    return  newuser