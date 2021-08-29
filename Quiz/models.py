from django.db import models
from django.db.models.fields.related import OneToOneField
from django.contrib.auth.models import User
import random


class Pregunta(models.Model):
    texto = models.TextField(verbose_name='Contenido de la pregunta')
    max_puntaje = models.DecimalField(verbose_name='Puntaje máximo', default=3, decimal_places=2, max_digits=6)

    def __str__(self):
        return self.texto


class Respuesta(models.Model):
    # Cantidad máxima y mínima de opciones/respuestas por pregunta
    MAX = 4
    MIN = 4
    pregunta = models.ForeignKey(Pregunta, related_name='opciones', on_delete=models.CASCADE)
    correcta = models.BooleanField(verbose_name='¿Es la respuesta correcta?', default=False, null=False)
    texto = models.TextField(verbose_name='Contenido de la respuesta')

    def __str__(self):
        return self.texto


class QuizUsuario(models.Model):
    # Cascade para que cuando se elimine un usuario, se eliminen las preguntas respondidas y otras asociaciones del mismo
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario')
    puntaje_total = models.DecimalField(verbose_name='Puntaje Total', default=0, decimal_places=2, max_digits=10, null=True)
    fecha_de_creacion = models.DateTimeField(auto_now_add=True)

    def crear_intentos(self, pregunta):
        intento = PreguntasRespondidas(pregunta=pregunta, quizUser=self)
        intento.save()

    def obtener_nuevas_preguntas(self):
        respondidas = PreguntasRespondidas.objects.filter(quizUser=self).values_list('pregunta__pk', flat=True)
        preguntas_restantes = Pregunta.objects.exclude(pk__in=respondidas)
        if not preguntas_restantes.exists():
            return None
        return random.choice(preguntas_restantes)
    
    # Respuesta Seleccionada es de la clase Respuesta de este mismo archivo (models)
    def validar_intento(self, pregunta_respondida, respuestas_seleccionadas, opciones_correctas):
        for res in respuestas_seleccionadas:
            if pregunta_respondida.pregunta_id != res.pregunta_id:
                return
        
        pregunta_respondida.respuesta_seleccionada = respuestas_seleccionadas
        valor = respuestas_seleccionadas[0].pregunta.max_puntaje / opciones_correctas
        for res in respuestas_seleccionadas:
            if res.correcta is True:
                pregunta_respondida.correcta = True
                pregunta_respondida.puntaje = pregunta_respondida.puntaje + valor
            else:
                # Si una de las respuestas elegidas no es correcta, se le descuenta un punto
                pregunta_respondida.puntaje = pregunta_respondida.puntaje - 1
        
        pregunta_respondida.respuesta.set(respuestas_seleccionadas)
        pregunta_respondida.save()
        self.actualizar_puntaje()
    
    def actualizar_puntaje(self):
        # Hacemos una operación de agregación entre los registros de la base de datos que sume el puntaje obtenido en cada respuesta del usuario
        puntaje_actualizadoTrue = self.intentos.filter(correcta=True).aggregate(models.Sum('puntaje'))['puntaje__sum']
        puntaje_actualizadoFalse = self.intentos.filter(correcta=False).aggregate(models.Sum('puntaje'))['puntaje__sum']
        if puntaje_actualizadoTrue is None:
            puntaje_actualizadoTrue = 0
        if puntaje_actualizadoFalse is None:
            puntaje_actualizadoFalse = 0
        puntaje_actualizado = puntaje_actualizadoTrue - abs(puntaje_actualizadoFalse)
        if puntaje_actualizado < 0:
            puntaje_actualizado = 0
        
        # Actualizamos el puntaje
        self.puntaje_total = puntaje_actualizado
        self.save()


class PreguntasRespondidas(models.Model):
    quizUser = models.ForeignKey(QuizUsuario, on_delete=models.CASCADE, related_name='intentos')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='pregunta_intento')
    respuesta = models.ManyToManyField(Respuesta)
    correcta = models.BooleanField(verbose_name='¿Es la respuesta correcta?', default=False, null=False)
    puntaje = models.DecimalField(verbose_name='Puntaje Obtenido', default=0, decimal_places=2, max_digits=6)