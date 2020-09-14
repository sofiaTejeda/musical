import time
from datetime import timedelta
from uuid import uuid4

from firebase_admin import firestore, initialize_app, credentials
from polls.grupo import Grupo, User, GrupoEncoder
from os import path
import firebase_admin
from polls.cancion import Cancion, CancionEncoder
import json
from json import JSONEncoder

class GrupoService:
    __module__ : 'GrupoService'
    
    __all__ = ['getGrupoByUsuario']
    
    def __init__(self):
        basepath = path.dirname(__file__)
        dir = path.join(basepath,'..','sistemarecomendaciongrupos.json')
        #self._cred = credentials.Certificate(u'F:/tesis/web-service/sistemaRecomendacion/sistemarecomendaciongrupos.json')
        self._cred =  credentials.Certificate(dir)
        #print(firebase_admin._DEFAULT_APP_NAME)
        if (firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps): initialize_app(self._cred)
        self._db = firestore.client()

    def getGrupoById(self, id):
        group = self._db.collection(u'grupos').document(id).get()
        users = self._db.collection(u'grupos').document(id).collection('users').stream()

        usersArray = []
        for user in users:
            us = User.from_dict(user.to_dict())
            usersArray.append(us)

        gr = Grupo(group.to_dict()['name'], usersArray)        

        return gr

    def getGrupoByUsuario(self, user):        
        info = []

        grupo = self._db.collection_group(u'users').where(u'id', u'==', user)
        docs = grupo.stream()

        for doc in docs:
            info.append(doc.reference.parent.parent.id)

        jsonStr = None
        if(len(info) > 0): 
            idGrupo = info[0]
            jsonStr = self.getGrupoById(idGrupo)
            #jsonStr = json.dumps(dataJson, indent=4 ,cls=GrupoEncoder)

        return jsonStr

    def getCanciones(self):
        listCanciones = []
        listCanciones.append(Cancion(1,"Nothing else metters","Metallica", "9999","9999",10,10,1))
        listCanciones.append(Cancion(2,"Enter Sandman","Metallica", "9999","9999",10,10,1))
        listCanciones.append(Cancion(3,"The Unforgive","Metallica", "9999","9999",10,10,1))
        listCanciones.append(Cancion(4,"Too Much Heaven","Bee Gees", "9999","9999",10,10,1))
        listCanciones.append(Cancion(5,"How Deep Is Your Love","Bee Gees", "9999","9999",10,10,1))
        listCanciones.append(Cancion(6,"Stayin Alive","Bee Gees", "9999","9999",10,10,1))
        listCanciones.append(Cancion(7,"Nunca es Suficiente","Los Angeles Azules", "9999","9999",10,10,1))

        dataJson = json.dumps(listCanciones, indent=4 ,cls=CancionEncoder)
        return dataJson
    
    def saveUsuarios(self):
        users = self._db.collection_group(u'users').stream()

        userTemp = {}
        for user in users:
            userFire = user.to_dict()
            userTemp = {u'id': userFire['id'], u'usado': False}
            #doc_ref = self._db.collection(u'grupos').document()       

            try :
                self._db.collection('usuarioDisponibles').add(userTemp)
            except:
                print('error')
    
    def getInitUsuarioDisponible(self, idUsuario):
        user = self._db.collection(u'usuarioDisponibles').where(u'usado', u'==', False).limit(1).stream()
        userFirebase = self.getFirstUsuarioDisponible(idUsuario)
        userFire = {'id' : None}
        #if(len(user) > 0):
        if(userFirebase['idFirebase'] == None):
            for u in user:
                userFire = u.to_dict()
                id = u.id

                userDocument = self._db.collection(u'usuarioDisponibles').document(id)
                userDocument.update({ 'usado':True })

                usuarioDocument = self._db.collection(u'usuarios').document()
                usuarioDocument.set({u'idFirebase': idUsuario, 'idRecomendacion': userFire['id']})
        else: 
            userFire['id'] = userFirebase['idRecomendacion']

        return userFire['id']
    
    def getFirstUsuarioDisponible(self, idUsuario):
        user = self._db.collection(u'usuarios').where(u'idFirebase', u'==', idUsuario).limit(1).stream()
        
        userFire = {'idFirebase' : None}
        #if(len(user) > 0):
        for u in user:
            userFire = u.to_dict()

        return userFire





