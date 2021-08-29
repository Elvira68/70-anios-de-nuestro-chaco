from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import inicio, registro, userLogin, userLogout, home, jugar, resultado_pregunta, tablero, borrarJuego

urlpatterns = [
    path('', home, name=''),
    path('home/', home, name='home'),
    path('registro/', registro, name='registro'),
    path('login/', userLogin, name='login'),
    path('logout/', userLogout, name='logout'),
    path('play/', jugar, name='jugar'),
    path('resultado/<int:pregunta_respondida_pk>', resultado_pregunta, name='resultado'),
    path('tablero/', tablero, name='tablero'),
    path('borrarJuego/', borrarJuego, name='borrarJuego'),
]
