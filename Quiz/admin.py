from django.contrib import admin

from .models import Pregunta, Respuesta

class RespuestaInline(admin.TabularInline):
    can_delete = False
    model = Respuesta
    max_num = Respuesta.MAX
    min_num = Respuesta.MIN

class PreguntaAdmin(admin.ModelAdmin):
    model = Pregunta
    inlines = (RespuestaInline,)
    list_display = ['texto',]
    search_fields = ['texto', 'preguntas__texto']

admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(Respuesta)