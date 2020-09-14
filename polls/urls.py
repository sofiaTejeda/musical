from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('getGrupo', views.getGrupo, name='getGrupo'),
    path('getCanciones', views.getCanciones, name='getCanciones'),
    path('getTestRecomendacion', views.getTestRecomendacion, name='getTestRecomendacion'),
    path('getsaveUsuarios', views.getsaveUsuarios, name='getsaveUsuarios'),
    path('getFirstUsuarioDisponible', views.getFirstUsuarioDisponible, name='getFirstUsuarioDisponible'),
    path('getInitUsuarioDisponible', views.getInitUsuarioDisponible, name='getInitUsuarioDisponible'),






]