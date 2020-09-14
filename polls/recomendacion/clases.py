from enum import Enum
from json import JSONEncoder

class GrupoUsuario():
    def __init__(self, usuarios,canciones):
        self.Usuarios=usuarios
        self.Canciones = canciones
        self.Prediccion=[]
        self.Identificador=0
        self.RMSE=0
        self.MSE=0
        self.Evaluado=0
        self.MAE=0

class TipoAgregacion(Enum):
    LM = 1
    MP = 2
    AV = 3


class TipoError(Enum):
    RMSE = 1
    MAE = 2
    MSE = 3


class PrediccionAgregacion():
    def __init__(self, score,tipoagregacion):
        self.Score=score
        self.TipoAgregacion=tipoagregacion

class EvalResults():
    def __init__(self, descripcion,valor,tipo,tipogrupo,estrategia):
        self.Descripcion=descripcion
        self.Valor = valor
        self.TipoError=tipo
        self.TipoGrupo=tipogrupo
        self.Estrategia=estrategia


    
class Usuario():
    def __init__(self, usuarioid,canciones):
        self.UsuarioId=usuarioid
        self.Canciones = canciones
        self.RMSE=0
        self.MAE=0
        self.MSE=0
        self.Evaluado=0
        self.Recomendaciones=[]

class UsuarioArmarGrupo():
    def __init__(self, usuarioid,ratingsongs):
        self.UsuarioId=usuarioid
        self.RatingSongs=ratingsongs
        self.CancionRecomendar=[]
        self.RMSE=0
        self.Evaluado=0
        self.Canciones = []

class Cancion():
    def __init__(self, songid,nombre,listencount):
        self.SongId=songid
        self.Nombre= nombre
        self.ArtistName=""
        self.Release=""
        self.Year=0
        self.ListenCount=listencount
        self.MeanSong=0
        self.SongPred=0


class Recomendacion():

    def __init__(self, cancionesc,cancionrecomendada):
        self.CancionEscuchada=cancionesc
        self.CancionRecomendada=cancionrecomendada
    
    def to_dict(self):
        return {u'CancionEscuchada': self.CancionEscuchada, u'CancionRecomendada': self.CancionRecomendada }

    def __repr__(self):
        return(
            f'Recomendacion(CancionEscuchada={self.CancionEscuchada},CancionRecomendada={self.CancionRecomendada})'
        )
  
class RecomendacionEncoder(JSONEncoder):
        def default(self, o): return o.__dict__     


class UsuarioCoseno():
    def __init__(self, usuarioid,similarity,mean,rating,correlation,sumsimilarity):
        self.UsuarioId=usuarioid
        self.Similarity= similarity
        self.Mean=mean
        self.Ratings=rating
        self.SumSimilarity=sumsimilarity
        self.Correlation=correlation

