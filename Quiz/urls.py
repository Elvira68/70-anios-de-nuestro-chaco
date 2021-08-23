from django.urls import path
from .views import inicio, registro, userLogin, userLogout, home, jugar

urlpatterns = [
    path('', inicio, name='inicio'),
    path('home/', home, name='home'),
    path('registro/', registro, name='registro'),
    path('login/', userLogin, name='login'),
    path('logout/', userLogout, name='logout'),
    path('play/', jugar, name='jugar'),
]
