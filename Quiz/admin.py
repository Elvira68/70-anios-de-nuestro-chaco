import json
from django.contrib import admin
from django.db.models.functions import TruncDay
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from .models import Pregunta, Respuesta, PreguntasRespondidas, QuizUsuario

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

class PreguntasRespondidasAdmin(admin.ModelAdmin):
    list_display = ['pregunta', 'respuesta', 'correcta', 'puntaje']

    class Meta:
        model = PreguntasRespondidas


@admin.register(QuizUsuario)
class Estadísticas(admin.ModelAdmin):
    list_display = ("id", "usuario_id", "puntaje_total", "fecha_de_creacion") # Renderizar estos datos en vistas de columnas
    ordering = ("-fecha_de_creacion",)                  # Ordenarlos por fecha de creación

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = (
            QuizUsuario.objects.annotate(date=TruncDay("fecha_de_creacion"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(PreguntasRespondidas)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(Respuesta)
# admin.site.register(QuizUsuario)
# admin.site.register(Estadísticas)