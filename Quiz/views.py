from typing import ContextManager
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Count
from django.db.models.expressions import Case, When
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegistroFormulario, LoginFormulario
from .models import QuizUsuario, Pregunta, PreguntasRespondidas
from django.contrib.auth.decorators import login_required


def inicio(request):
    context = {
        'bienvenidoValue': 'Bienvenido'
    }
    return render(request, 'inicio.html', context)


def home(request):
    return render(request, 'usuario/home.html')


def userLogin(request):
    titulo = 'Iniciar sesión'

    form = LoginFormulario(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        usuario = authenticate(username=username, password=password)
        login(request, usuario)
        return redirect('home')

    context = {
        'form': form,
        'titulo': titulo,
    }

    return render(request, 'usuario/login.html', context)


def userLogout(request):
    logout(request)
    return redirect('home')

def borrarJuego(request):
    QuizUsuario.objects.get(usuario=request.user).delete()
    return redirect('jugar')


def registro(request):
    titulo = 'Crear una cuenta'

    if request.method == 'POST':
        form = RegistroFormulario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroFormulario()

    context = {
        'form': form,
        'titulo': titulo
    }

    return render(request, 'usuario/registro.html', context)


@login_required(login_url='/login/')
def jugar(request):
    QuizUser, created = QuizUsuario.objects.get_or_create(usuario=request.user)
    opciones_correctas = 1

    if request.method == 'POST':
        pregunta_pk = request.POST.get('pregunta_pk')
        pregunta_respondida = QuizUser.intentos.select_related(
            'pregunta').get(pregunta__pk=pregunta_pk)
        respuestas_pk = request.POST.getlist('respuesta_pk')
        preg = Pregunta.objects.get(pk=pregunta_pk)

        try:
            list = []
            for i in respuestas_pk:
                list.append(pregunta_respondida.pregunta.opciones.get(
                pk=i))
        except ObjectDoesNotExist:
            raise Http404

        opciones_correctas = preg.opciones.aggregate(correctas=Count(Case(When(correcta=1, then=1))))
        QuizUser.validar_intento(pregunta_respondida, list, opciones_correctas['correctas'])

        return redirect('resultado', pregunta_respondida.pk)

    else:
        pregunta = QuizUser.obtener_nuevas_preguntas()
        if pregunta is not None:
            QuizUser.crear_intentos(pregunta)
        
        posicion = QuizUsuario.objects.filter(puntaje_total=QuizUser.puntaje_total).aggregate(ranking=Count('puntaje_total'))

        context = {
            'posicion': posicion['ranking'],
            'post': request.POST,
            'puntaje_total': QuizUser.puntaje_total,
            'pregunta': pregunta
        }

    return render(request, 'play/play.html', context)


def resultado_pregunta(request, pregunta_respondida_pk):
    respondida = get_object_or_404(
        PreguntasRespondidas, pk=pregunta_respondida_pk)
    context = {
        'respondida': respondida
    }
    return render(request, 'play/resultados.html', context)


def tablero(request):
    total_usaurios_quiz = QuizUsuario.objects.order_by('-puntaje_total')[:10]
    contador = total_usaurios_quiz.count()

    context = {
        'usuario_quiz': total_usaurios_quiz,
        'contar_user': contador
    }

    return render(request, 'play/tablero.html', context)

