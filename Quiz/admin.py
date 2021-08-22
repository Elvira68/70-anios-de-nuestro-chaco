from django.contrib import admin

from .models import Pregunta, Respuesta

admin.site.register(Pregunta)
admin.site.register(Respuesta)