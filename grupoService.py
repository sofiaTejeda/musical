import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from grupo import Grupo, User

class GrupoService:
    __module__ : 'GrupoService'
# _cred = credentials.Certificate('F:/tesis/python-firebase/firebase/recomendaciongrupos-firebase-adminsdk-n5rkf-d9a9e65432.json')
# _db
    def __init__(self):
        self._cred = credentials.Certificate('sistemarecomendaciongrupos-firebase-adminsdk-uz0rg-e1d4e0482a.json')
        firebase_admin.initialize_app(self._cred)
        self._db = firestore.client()

    def saveUser(self, group):
        doc_ref = self._db.collection(u'grupos').document()
        doc_ref.set(group.to_dict())

        for user in group.to_dict_user():
            try :
                doc_ref.collection('users').add(user)
            except:
                print('error')


    def getGrupos(self):
        groups = self._db.collection(u'grupos').stream()
        #for user in users
        groupsArray = []
        for group in groups:
            users = self._db.collection(u'grupos').document(group.id).collection('users').stream()            

            usersArray = []
            for user in users:
                us = User.from_dict(user.to_dict())
                usersArray.append(us)

            gr = Grupo(group.to_dict(), usersArray)
            groupsArray.append(gr)

        return groupsArray

    def getGrupoById(self, id):
        group = self._db.collection(u'grupos').document(id).get()
        users = self._db.collection(u'grupos').document(id).collection('users').stream()
        usersArray = []
        for user in users:
            us = User.from_dict(user.to_dict())
            usersArray.append(us)
        gr = Grupo(group.to_dict(), usersArray)        
        return gr

    def getGrupoByUsuario(self, user):        
        info = []

        grupo = self._db.collection_group(u'users').where(u'id', u'==', user)
        docs = grupo.stream()

        for doc in docs:
            print(u'{} => {}'.format(doc.id, doc.to_dict()))         
            #grupoTemp = self._db.collection(u'grupos').document(doc.reference.parent.parent.id).get()
            info.append(doc.reference.parent.parent.id)

        dataJson = None
        if(len(info) > 0): 
            idGrupo = info[0]
            dataJson = self.getGrupoById(idGrupo)
            
        return dataJson
    
    
    

        #print(users)
            
        
