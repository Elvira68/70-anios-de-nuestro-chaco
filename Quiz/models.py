from django.db import models
from django.db.models.fields.related import OneToOneField
from django.contrib.auth.models import User


class Pregunta(models.Model):
    texto = models.TextField(verbose_name='Contenido de la pregunta')

    def __str__(self):
        return self.texto


class Respuesta(models.Model):
    # Cantidad máxima y mínima de opciones/respuestas por pregunta
    MAX = 4
    MIN = 4
    pregunta = models.ForeignKey(Pregunta, related_name='preguntas', on_delete=models.CASCADE)
    correcta = models.BooleanField(verbose_name='¿Es la respuesta correcta?', default=False, null=False)
    texto = models.TextField(verbose_name='Contenido de la respuesta')

    def __str__(self):
        return self.texto


class QuizUsuario(models.Model):
    # Cascade para que cuando se elimine un usuario, se eliminen las preguntas respondidas y otras asociaciones del mismo
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    puntaje_total = models.IntegerField(verbose_name='Puntaje Total', default=0)


class PreguntasRespondidas(models.Model):
    quizUser = models.ForeignKey(QuizUsuario, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(Respuesta, on_delete=models.CASCADE, related_name='intentos')
    correcta = models.BooleanField(verbose_name='¿Es la respuesta correcta?', default=False, null=False)
    puntaje = models.IntegerField(verbose_name='Puntaje obtenido', default=0)