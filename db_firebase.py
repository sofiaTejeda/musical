import sys
import os
import numpy as np
from grupoService import GrupoService
from grupo import Grupo, User
import BuildGraph as bg
import clases as cs

def CreateGrupos(grupos):
    
    grupoService = GrupoService()
    for i in grupos:
        users = []
        for j in i.Usuarios:
            users.append(User(j.UsuarioId))        
        grupoService.saveUser(Grupo(i.Identificador,users))
        
    
def GetGrupos():
    grupoService = GrupoService()
    grupos = grupoService.getGrupos()
    #print(grupos)
    return grupos    

def GetGruposByUsuario(userid):
    grupoService = GrupoService()
    grupos = grupoService.getGrupoByUsuario(userid)
    return grupos
    