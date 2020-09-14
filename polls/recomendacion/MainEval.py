from polls.recomendacion import Prediction
from polls.recomendacion import BuildGraph as bg
from polls.recomendacion import clases as cs
from polls.recomendacion import EvalMetrics as rmse
import pandas as pd
import statistics
import scipy.sparse as sp
from scipy.sparse.linalg import svds
from surprise import SVD
from surprise import accuracy
from surprise.model_selection import train_test_split
import os
from surprise import Reader, Dataset
import numpy as np
from os import path

class Main:
    def __init__(self):
        self.Canciones = []
        self.UserRating=[]
        
    def LoadDataEval(self):
        basepath = path.dirname(__file__)
        song_data = path.join(basepath,r'DatasetMusica/song_data.csv')
        millionsong = path.join(basepath,r'DatasetMusica/millionsong.csv')
        traindata = path.join(basepath,r'traindata.csv')
        testdata = path.join(basepath,r'traindata.csv')

        self.Canciones = pd.read_csv(song_data)
        self.UserRating= pd.read_csv(millionsong)
        self.TrainRating=pd.read_csv(traindata)
        self.TestRating=pd.read_csv(testdata)
        
    def LoadDataRecomender(self):
        basepath = path.dirname(__file__)
        dir = path.join(basepath,r'DatasetMusica/song_data.csv')
        self.Canciones = pd.read_csv(dir)
        subset = path.join(basepath,r'subset2.csv')
        data=pd.read_csv(subset)
        self.UserRating=data
        print('No. Unico Usuarios    :', self.UserRating.user_id.nunique())
        print('No. Unico Canciones :', self.UserRating.song_id.nunique()) 
        print('No. Unico de Escuchas  :', self.UserRating.listen_count.nunique())
    
    def PreprocessData(self,f):
        users= self.TrainRating[['user_id']]
        users=users.drop_duplicates()
        users = users.sample(frac = 1)
        users=users.head(f)
        #self.TrainRating=self.TrainRating[self.TrainRating['user_id'].isin(users['user_id'].tolist())]

        dictmusicprepared= {
        'song_id': (self.TrainRating.song_id),
        'user_id': list(self.TrainRating.user_id),
        'rating': list(self.TrainRating.listen_count)}
        reader= Reader(rating_scale=(1, 100))
        dftrain=pd.DataFrame(dictmusicprepared)
        self.DataMusicTrain=Dataset.load_from_df(dftrain[['user_id', 'song_id', 'rating']], reader)
        self.GrupoSimilar=[]
        self.GrupoAleatorio=[]

    def TrainTestData(self):
        #train_data, test_data = train_test_split(self.DataMusicTrain, test_size=.20)            
        #self.TestDataUse=pd.DataFrame(test_data.copy(), columns=['user_id', 'song_id','rating'])
        test=self.TestRating.values.tolist()
        test_data=test.copy()
        train_data=self.DataMusicTrain.build_full_trainset()
        self.TestDataUse=pd.DataFrame(test_data.copy(), columns=['user_id', 'song_id','rating'])
        return train_data,test_data


    def GetDataByGrupo(self):
        return self.UserRating, self.Canciones
      
    def PreprocessDataPredictor(self):
        dictmusicprepared= {
        'song_id': (self.UserRating.song_id),
        'user_id': list(self.UserRating.user_id),
        'rating': list(self.UserRating.listen_count)}
        reader= Reader(rating_scale=(1, 100))
        dftrain=pd.DataFrame(dictmusicprepared)
        datatrain= Dataset.load_from_df(dftrain[['user_id', 'song_id', 'rating']], reader)
        trainsetfull = datatrain.build_full_trainset()
        self.FinalRatingSVD=trainsetfull
    
        

    def CreateGroupsWithSimilaritiesFunc(self):
        usertrain=self.FinalRatingSVD._raw2inner_id_users
        df1 = pd.DataFrame(usertrain.keys()) 
        df1=df1[df1.columns[0]].unique()
        pr = Prediction.BasePrediction(self.FinalRatingSVD,[])
        modelcosine, similaritymatriz=pr.CalcularMatrizSimilaridad()
        self.ModelCosine=modelcosine
        usergroups=bg.ArmarGruposDefSimilaresFunc(df1,self.FinalRatingSVD,similaritymatriz)
        return usergroups


    def CreateGroupsWithSimilaritiesEval(self, train, test):
        if(self.GrupoSimilar==[]):
            dftest=self.TestDataUse[["user_id"]]
            dftest=dftest['user_id'].unique()
            usertrain=train._raw2inner_id_users
            listuser=[]
            df1 = pd.DataFrame(usertrain.keys()) 
            df1=df1[df1.columns[0]].unique()
            pr = Prediction.BasePrediction(train,[])
            modelcosine, similaritymatriz=pr.CalcularMatrizSimilaridad()
            self.ModelCosine=modelcosine
            usergroups=bg.ArmarGruposDefSimilaresEval(df1, self.Canciones,train,self.TestDataUse,similaritymatriz)
            self.GrupoSimilar=usergroups.copy()
            return usergroups.copy()
        else:
            return self.GrupoSimilar.copy()
        
        
    def CreateGroupsAleatoriosEval(self,train,test):
        if(self.GrupoAleatorio==[]):
            dftest=self.TestDataUse[["user_id"]]
            dftest=dftest['user_id'].unique()
            usertrain=train._raw2inner_id_users
            listuser=[]
            df1 = pd.DataFrame(usertrain.keys()) 
            df1=df1[df1.columns[0]].unique()
            usergroups=bg.ArmarGruposDefAleatorioEval(df1, self.Canciones,train,self.TestDataUse)
            self.GrupoAleatorio=usergroups.copy()
            return usergroups.copy()
        else:
            return self.GrupoAleatorio.copy()    
 
    def EvalCosineAlgorithm(self):
        train,test=self.TrainTestData()
        grupoaleatorio=self.CreateGroupsAleatoriosEval(train,test)
        gruposimilar=self.CreateGroupsWithSimilaritiesEval(train,test)
        pr = Prediction.BasePrediction(train,test)
        model,result=pr.CosineAlgorithmSurprise()
        Listgrupos=[]
        usuariorecommend=[] 
        """rmsetotal,meatotal,msetotal=self.EvalGrupo(model,result,grupoaleatorio)
        rmsetotal1,meatotal1,msetotal1=self.EvalGrupo(model,result,gruposimilar)
        """
        
        result1=self.EvalGrupo(model,result,grupoaleatorio,"GA",1,"COS")
        result2=self.EvalGrupo(model,result,gruposimilar,"SM",2,"COS")
        lstresultado=[]
        for i in result1:
            lstresultado.append(i)
        for i in result2:
            lstresultado.append(i)

       
        return lstresultado
    
    def EvalSvdAlgorithm(self,k):
        train,test=self.TrainTestData()
        grupoaleatorio=self.CreateGroupsAleatoriosEval(train,test)
        gruposimilar=self.CreateGroupsWithSimilaritiesEval(train,test)
        pr = Prediction.BasePrediction(train,test)
        model,result=pr.SVDAlgorithmPredict(k)
        Listgrupos=[]
        usuariorecommend=[] 
        result1=self.EvalGrupo(model,result,grupoaleatorio,"GA",1,"SVD")
        result2=self.EvalGrupo(model,result,gruposimilar,"SM",2,"SVD")
        lstresultado=[]
        for i in result1:
            lstresultado.append(i)
        for i in result2:
            lstresultado.append(i)

        return lstresultado 

    def AgregationStrategies(self,estrategia,canciongrupo,usuarios):
        cancionesscore=[]
        if(estrategia==1):
            for c in canciongrupo:                
                score=[]
                evaluado=0
                for y in usuarios:
                    resp= next((l for l in y.CancionRecomendar if l.SongId==c.SongId), None)
                    if resp is not None:
                        score.append(resp.SongPred)
                minval=min(score)
                newcancion=cs.Cancion(c.SongId,"title",minval)
                newcancion.SongPred=minval
                cancionesscore.append(newcancion)    
        
        if(estrategia==3):
            for c in canciongrupo:                
                score=[]
                evaluado=0
                for y in usuarios:
                    resp= next((l for l in y.CancionRecomendar if l.SongId==c.SongId), None)
                    if resp is not None:
                        score.append(resp.SongPred)
                meanval=statistics.mean(score)
                newcancion=cs.Cancion(c.SongId,"title",meanval)
                newcancion.SongPred=meanval
                cancionesscore.append(newcancion)            
        
        if(estrategia==2):
            for c in canciongrupo:                
                score=[]
                evaluado=0
                for y in usuarios:
                    resp= next((l for l in y.CancionRecomendar if l.SongId==c.SongId), None)
                    if resp is not None:
                        score.append(resp.SongPred)
                maxval=max(score)
                newcancion=cs.Cancion(c.SongId,"title",maxval)
                newcancion.SongPred=maxval
                cancionesscore.append(newcancion)            

        return cancionesscore


    def EvalGrupo(self,model,result,groups,tipogrupodescripcion,tipogrupo,algoritmo):
        k=1
        for x in groups:
            usuariogrupo=[]
            cancionusuario=[]
            
            for y in x.Usuarios:
                userpred=result[result.user_id==y.UsuarioId]
                bg.RecommendSongsEvalAlgorithm(y, userpred,model)      
            canciongrupo= x.Canciones
            cancionesscoreLM=self.AgregationStrategies(1,canciongrupo,x.Usuarios)
            cancionesscoreAV=self.AgregationStrategies(3,canciongrupo,x.Usuarios)
            cancionescoreMP=self.AgregationStrategies(2,canciongrupo,x.Usuarios)
            """print("LM")
            for i in cancionesscoreLM:
                print(i.SongPred)
            print("AV")
            for i in cancionesscoreAV:
                print(i.SongPred)

            print("MP")
            for i in cancionescoreMP:
                print(i.SongPred)"""


            x.Prediccion=[]
            x.Prediccion.append(cs.PrediccionAgregacion(cancionesscoreLM,1))
            x.Prediccion.append(cs.PrediccionAgregacion(cancionesscoreAV,3))
            x.Prediccion.append(cs.PrediccionAgregacion(cancionescoreMP,2))
        
        evalresults=[]

        rmsetotal,meatotal,msetotal=rmse.RMSEGrupos(groups,1)
     
        evalresults.append(cs.EvalResults(algoritmo+" LM "+tipogrupodescripcion,rmsetotal,1,tipogrupo,1))        
        evalresults.append(cs.EvalResults(algoritmo+" LM "+tipogrupodescripcion,meatotal,2,tipogrupo,1))
        evalresults.append(cs.EvalResults(algoritmo+" LM "+tipogrupodescripcion,msetotal,3,tipogrupo,1))

        
        rmsetotal2,meatotal2,msetotal2=rmse.RMSEGrupos(groups,2)
        evalresults.append(cs.EvalResults(algoritmo+" MP "+tipogrupodescripcion,rmsetotal2,1,tipogrupo,2))        
        evalresults.append(cs.EvalResults(algoritmo+" MP "+tipogrupodescripcion,meatotal2,2,tipogrupo,2))
        evalresults.append(cs.EvalResults(algoritmo+" MP "+tipogrupodescripcion,msetotal2,3,tipogrupo,2))

      
        rmsetotal3,meatotal3,msetotal3=rmse.RMSEGrupos(groups,3)
        evalresults.append(cs.EvalResults(algoritmo+" AV "+tipogrupodescripcion,rmsetotal3,1,tipogrupo,3))        
        evalresults.append(cs.EvalResults(algoritmo+" AV "+tipogrupodescripcion,meatotal3,2,tipogrupo,3))
        evalresults.append(cs.EvalResults(algoritmo+" AV "+tipogrupodescripcion,msetotal3,3,tipogrupo,3))

      
        return evalresults

    def SvdAlgorithm(self,k):
        pr = Prediction.BasePrediction(self.FinalRatingSVD,[])
        model=pr.SvdAlgorithmFunc(k)
        return model



