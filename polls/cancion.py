import json
from json import JSONEncoder


class Cancion(object):
    __module__ : 'Cancion'

    def __init__(self, songid,nombre, artistName, release, year,listencount, meanSong, songPred):
        self.SongId=songid
        self.Nombre= nombre
        self.ArtistName=artistName
        self.Release=release
        self.Year=0
        self.ListenCount=listencount
        self.MeanSong=0
        self.SongPred=0
    
    @staticmethod
    def from_dict(SongId, Nombre, ArtistName, Release, Year, ListenCount, MeanSong, SongPred):
        cancion = Cancion(SongId, Nombre, ListenCount)
        return cancion

    def to_dict(self):
        return {u'songId': self.SongId,
        u'nombre': self.Nombre,
        u'artistName':self.ArtistName,
        u'release':self.Release,
        u'year':self.Year,
        u'listenCount':self.ListenCount,
        u'meanSong':self.MeanSong,
        u'songPred':self.SongPred,
        }    

class CancionEncoder(JSONEncoder):
    def default(self, o): return o.__dict__