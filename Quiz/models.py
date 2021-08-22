from django.db import models

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