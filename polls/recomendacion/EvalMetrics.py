import sklearn
import numpy as np
import pandas as pd
from polls.recomendacion import clases as cs
import math

def RMSEGrupos(groups, agregacion):
    
    print("agregacion: "+str(agregacion))
    evaluadogrupo=0
    rmsetotal=0;
    msetotal=0
    meatotal=0
    l = []
    i=0;
    
    for g in groups:
        rmsegrupo=0
        msegrupo=0
        meagrupo=0
        evaluado=0
        k=1
        for u in g.Usuarios:
            actual=[]
            pred=[]
            for song in u.Canciones:
                actual.append(song.ListenCount)
                
                prediccion=next((l for l in g.Prediccion if l.TipoAgregacion==agregacion), None)
               
                scorepred=next((l for l in prediccion.Score if l.SongId==song.SongId), None)
                if scorepred is not None:
                    pred.append(scorepred.SongPred)
                    song.SongPred=scorepred.SongPred
                else:
                    pred.append(0)                    
                    
            if len(actual)>0 and len(pred)>0:
                               
                mse = sklearn.metrics.mean_squared_error(actual,pred)
                mae = sklearn.metrics.mean_absolute_error(actual,pred)
                rmse = math.sqrt(mse)
                """u.RMSE=rmse
                u.MSE=mse
                u.MAE=mae
                u.Evaluado=1"""
                rmsegrupo+=rmse
                msegrupo+=mse
                meagrupo+=mae 
                evaluado+=1
        if(evaluado>1):
            rmsegrupo=rmsegrupo/evaluado
            msegrupo=msegrupo/evaluado
            meagrupo=meagrupo/evaluado
            """g.RMSE=rmsegrupo
            g.MAE=meagrupo
            g.MSE=msegrupo
            g.Evaluado=1"""
            evaluadogrupo+=1
            rmsetotal+=rmsegrupo
            msetotal+=msegrupo
            meatotal+=meagrupo
    if evaluadogrupo >0:
        rmsetotal=rmsetotal/evaluadogrupo
        meatotal=meatotal/evaluadogrupo
        msetotal=msetotal/evaluadogrupo
    return rmsetotal,meatotal,msetotal





