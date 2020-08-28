import db_firebase as db
import MainEval as maineval2
import BuildGraph as bg 
import statistics
import clases as cs

class Recommender:

    def __init__(self,totalusuarios,k):
        print("Initialize recommender")
        mn=maineval2.Main()
        mn.LoadDataRecomender()
        self.mn=mn
        self.mn.PreprocessDataPredictor()
        self.k=k
        self.data,self.canciones=mn.GetDataByGrupo()
        
        
    def CreateGrupo(self):
        grupos=self.mn.CreateGroupsWithSimilaritiesFunc()
        db.CreateGrupos(grupos)
    
    def GetGrupos(self):
        grupos=db.GetGrupos()
        return grupos

    def EvalAlgorithm(self, numrecomendation,usuarioId):
        grupousuario=db.GetGruposByUsuario(usuarioId)
        usuarios=[]
        for u in grupousuario.users:
            usuarios.append(u.id)
        model=self.mn.SvdAlgorithm(self.k)
        Listgrupos=[]
        usuariogrupo=[]
        usuariorecommend=[] 
        cancionesscore=[]
        listcanciones=[] 
        cancionesprohibidas=[]         
        songid=self.mn.UserRating["song_id"]
        songid=songid.unique()
        datasearcheable=self.mn.UserRating.set_index('user_id')
        ud=datasearcheable[datasearcheable.index == (usuarioId)]
        songescuchadaid=ud["song_id"].unique()
        cancionescuchada=self.canciones[self.canciones.song_id.isin(songescuchadaid)]
        canciones=[]
        for index, row in cancionescuchada.iterrows():
            cancion = cs.Cancion(row["song_id"], str(row["title"]),0)
            cancion.ArtistName=str(row["artist_name"])
            cancion.Release=str(row["release"])
            cancion.Year=row["year"]
            canciones.append(cancion)
        
        for y in usuarios:
            user_data = datasearcheable[datasearcheable.index == (y)]
            user_data=user_data["song_id"]
            for c in user_data:
                cancionesprohibidas.append(c)
        cancionesprohibidas=list(set(cancionesprohibidas))
        self.canciones=(self.canciones[self.canciones.song_id.isin(songid)])
        self.canciones=(self.canciones[~self.canciones.song_id.isin(cancionesprohibidas)])
        cancionusuario=[]
        for y in usuarios:
            usuario=  bg.RecommendNumSongs(model, y, self.canciones, 200)
            usuariogrupo.append(usuario)
            for c in usuario.Canciones:
                cancionusuario.append(c.SongId)
                listcanciones.append(c)          
            
        cancionusuario= list(dict.fromkeys(cancionusuario))
        
        for c in cancionusuario:
            score=[]
            for y in usuariogrupo:
                resp= next((l for l in y.Canciones if l.SongId==c), None)
                if resp is not None:
                    score.append(resp.ListenCount)
                else:
                    result=model.predict(y.UsuarioId, iid = c)
                    score.append(result.est)
            scoref=min(score)
            cancion=next((l for l in listcanciones if l.SongId==c), None)
            cancion.Score=scoref
            cancionesscore.append(cancion)
        cancionesscore=sorted(cancionesscore, key=lambda cancionuser: cancionuser.ListenCount,reverse=True) 
        cancionrecomendar=cancionesscore[0:numrecomendation]
        recomend=cs.Recomendacion(canciones,cancionrecomendar)
        return recomend
        


    def RecommenderSong(self,usuarioId):
        grupos=db.getGrupos()
        print(grupos)
