from django.urls import path
from .views import inicio, registro

urlpatterns = [
    path('', inicio, name='inicio'),
    path('registro/', registro, name='registro')
]
