from django.urls import path
from .views import inicio, registro, userLogin, userLogout

urlpatterns = [
    path('', inicio, name='inicio'),
    path('registro/', registro, name='registro'),
    path('login/', userLogin, name='login'),
    path('logout/', userLogout, name='logout'),
]
