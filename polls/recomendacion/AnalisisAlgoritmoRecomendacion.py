#%%
from polls.recomendacion import MainEval as maineval2
from polls.recomendacion import Recommender as rc
from polls.recomendacion import clases as cs
import random
import numpy
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt1
import matplotlib.pyplot as plt2
import statistics


def ReviewData():
    mn=maineval2.Main()
    mn.LoadDataEval()
    print(mn.UserRating.describe())
    print('No. Unico Usuarios    :', mn.UserRating.user_id.nunique())
    print('No. Unico Canciones :', mn.UserRating.song_id.nunique()) 
    print('No. Unico de Escuchas  :', mn.UserRating.listen_count.nunique())

def EscuchaDadoPorUsuarios():

    mn=maineval2.Main()
    mn.LoadDataEval()
    rts_gp = mn.UserRating.groupby(by=['listen_count']).agg({'user_id': 'count'}).reset_index()
    rts_gp.columns = ['ListenCount', 'Count']
    plt.barh(rts_gp.ListenCount, rts_gp.Count, color='royalblue')
    plt.title('Overall Count of ListenCount', fontsize=15)
    plt.xlabel('Count', fontsize=15)
    plt.ylabel('ListenCount', fontsize=15)
    plt.grid(ls='dotted')
    plt.show()

def filterByTipoRmseLM(error):
    if(error.TipoError==1):
        if(error.Estrategia==1):
            return True
        else:
            return False
        
    else:
        return False

def filterByTipoRmseAV(error):
    if(error.TipoError==1):
        if(error.Estrategia==3):
            return True
        else:
            return False
        
    else:
        return False        

def filterByTipoRmseMP(error):
    if(error.TipoError==1):
        if(error.Estrategia==2):
            return True
        else:
            return False
        
    else:
        return False        


def filterByTipoMAELM(error):
    if(error.TipoError==2):
        if(error.Estrategia==1):
            return True
        else:
            return False
        
    else:
        return False

def filterByTipoMAEAV(error):
    if(error.TipoError==2):
        if(error.Estrategia==3):
            return True
        else:
            return False
        
    else:
        return False

def filterByTipoMAEMP(error):
    if(error.TipoError==2):
        if(error.Estrategia==2):
            return True
        else:
            return False
        
    else:
        return False

def GraphPerformances():
    mn=maineval2.Main()
    mn.LoadDataEval()
    mn.PreprocessData(100)
    lstresult=mn.EvalCosineAlgorithm()
    lstresultsvd=mn.EvalSvdAlgorithm(60)
    for i in lstresult:
        print(i.Descripcion+": "+str(i.Valor))
    for i in lstresultsvd:
        print(i.Descripcion+": "+str(i.Valor))

    lstrmsealgorithm1=[]
    lstrmsealgorithm2=[]
    lstrmsealgorithm3=[]
    
    lstrmse1=[]
    lstrmse2=[]
    lstrmse3=[]
    lstmse=[]
    lstmae1=[]
    lstmae2=[]
    lstmae3=[]
    #errorrmsecoseno= filter(filterByTipoRmse, lstresult)
    #errorrmsesvd= filter(filterByTipoRmse, lstresultsvd)
    #errorcosenmae=filter(filterByTipoMAE, lstresult)
    #errorsvdmae=filter(filterByTipoMAE, lstresultsvd)
 
    #errorsvd= next((l for l in lstresultsvd if l.TipoError==1), None)
    errornuevormse1=[]
    errornuevormse2=[]
    errornuevormse3=[]
    
    errornuevomae1=[]    
    errornuevomae2=[]
    errornuevomae3=[]
    [errornuevormse1.append(res) for res in filter(filterByTipoRmseLM, lstresult)]
    [errornuevormse1.append(res) for res in filter(filterByTipoRmseLM, lstresultsvd)]
    [errornuevormse2.append(res) for res in filter(filterByTipoRmseAV, lstresult)]
    [errornuevormse2.append(res) for res in filter(filterByTipoRmseAV, lstresultsvd)]
    [errornuevormse3.append(res) for res in filter(filterByTipoRmseMP, lstresult)]
    [errornuevormse3.append(res) for res in filter(filterByTipoRmseMP, lstresultsvd)]
    

    [errornuevomae1.append(res) for res in filter(filterByTipoMAELM, lstresult)]
    [errornuevomae1.append(res) for res in filter(filterByTipoMAELM, lstresultsvd)]
    
    [errornuevomae2.append(res) for res in filter(filterByTipoMAEAV, lstresult)]
    [errornuevomae2.append(res) for res in filter(filterByTipoMAEAV, lstresultsvd)]
    
    [errornuevomae3.append(res) for res in filter(filterByTipoMAEMP, lstresult)]
    [errornuevomae3.append(res) for res in filter(filterByTipoMAEMP, lstresultsvd)]
   
   
    [lstrmsealgorithm1.append(res.Descripcion) for res in errornuevormse1]
    [lstrmsealgorithm2.append(res.Descripcion) for res in errornuevormse2]
    [lstrmsealgorithm3.append(res.Descripcion) for res in errornuevormse3]


    [lstrmse1.append(res.Valor) for res in errornuevormse1]
    [lstrmse2.append(res.Valor) for res in errornuevormse2]
    [lstrmse3.append(res.Valor) for res in errornuevormse3]
   
    rmse1 = [round(res, 4) for res in lstrmse1]
    rmse2=[round(res, 4) for res in lstrmse2]
    rmse3=[round(res, 4) for res in lstrmse3]
    [lstmae1.append(res.Valor) for res in errornuevomae1]    
    [lstmae2.append(res.Valor) for res in errornuevomae2]
    [lstmae3.append(res.Valor) for res in errornuevomae3]
    mae1=[round(res, 4) for res in lstmae1]
    mae2=[round(res, 4) for res in lstmae2]
    mae3=[round(res, 4) for res in lstmae3]
    plt.figure(figsize=(20,5))
    plt.subplot(1, 2, 1)
    plt.title('Comparasion de Algoritmo en RMSE', loc='left', fontsize=15)
    plt.plot(lstrmsealgorithm1, rmse1, label='RMSE', color='darkgreen', marker='o')
    plt.xlabel('Algoritmo Least Misery', fontsize=15)
    plt.ylabel('RMSE', fontsize=15)
    plt.legend()
    plt.grid(ls='dashed')    
        
    plt.subplot(1, 2, 2)
    plt.title('Comparison de Algorithmo en MAE ', loc='center', fontsize=15)
    plt.plot(lstrmsealgorithm1, mae1, label='MAE', color='navy', marker='o')
    plt.xlabel('Algoritmo Least Misery', fontsize=15)
    plt.ylabel('MAE', fontsize=15)
    plt.legend()
    plt.grid(ls='dashed')    
    plt.show()

    plt1.subplot(1, 2, 1)
    plt1.title('Comparacion de Algorithms en RMSE', loc='left', fontsize=15)
    plt1.plot(lstrmsealgorithm2, rmse2, label='RMSE', color='red', marker='o')
    plt1.xlabel('Algoritmo Average', fontsize=15)
    plt1.ylabel('RMSE', fontsize=15)
    plt1.legend()
    plt1.grid(ls='dashed')    
        
    plt1.subplot(1, 2, 2)
    plt1.title('Comparacion de Algorithms en MAE', loc='center', fontsize=15)
    plt1.plot(lstrmsealgorithm2, mae2, label='MAE', color='pink', marker='o')
    plt1.xlabel('Algoritmo Average', fontsize=15)
    plt1.ylabel('MAE', fontsize=15)
    plt1.legend()
    plt1.grid(ls='dashed')    
    plt1.show()

    plt2.subplot(1, 2, 1)
    plt2.title('Comparacion de Algorithms en RMSE', loc='left', fontsize=15)
    plt2.plot(lstrmsealgorithm3, rmse3, label='RMSE', color='yellow', marker='o')
    plt2.xlabel('Algoritmo Most Pleasure', fontsize=15)
    plt2.ylabel('RMSE', fontsize=15)
    plt2.legend()
    plt2.grid(ls='dashed')

    plt2.subplot(1, 2, 2)
    plt2.title('Comparacion de Algorithms en MAE', loc='center', fontsize=15)
    plt2.plot(lstrmsealgorithm3, mae3, label='MAE', color='green', marker='o')
    plt2.xlabel('Algoritmo Most Pleasure', fontsize=15)
    plt2.ylabel('MAE', fontsize=15)
    plt2.legend()
    plt2.grid(ls='dashed')    
            

    plt2.show()
    

    """plt.figure(figsize=(20,5))
    plt.subplot(1, 2, 1)
    plt.title('Comparasion de Algorithms en RMSE', loc='center', fontsize=15)
    plt.plot(lstrmsealgorithm1, rmse1, label='RMSE', color='darkgreen', marker='o')
    plt.xlabel('Algoritmo', fontsize=15)
    plt.ylabel('RMSE', fontsize=15)
    plt.legend()
    plt.grid(ls='dashed')    
        
    plt.subplot(1, 2, 2)
    plt.title('Comparison de Algorithmo en MAE', loc='center', fontsize=15)
    plt.plot(lstrmsealgorithm, mae, label='MAE', color='navy', marker='o')
    plt.xlabel('Algoritmo', fontsize=15)
    plt.ylabel('MAE', fontsize=15)
    plt.legend()
    plt.grid(ls='dashed')    

    plt.show()
    """

    """for i in lstresult:
        print(i.Descripcion+": "+str(i.Valor))
    lstresultsvd=mn.EvalSvdAlgorithm(60)
    for i in lstresultsvd:
        print(i.Descripcion+": "+str(i.Valor))"""

