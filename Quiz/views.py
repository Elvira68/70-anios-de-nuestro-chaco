from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .forms import RegistroFormulario, LoginFormulario
from .models import QuizUsuario, Pregunta, PreguntasRespondidas

def inicio(request):
    context = {
        'bienvenidoValue': 'Bienvenido'
    }
    return render(request, 'inicio.html', context)


def home(request):
    return render(request, 'usuario/home.html')


def userLogin(request):
    titulo='Iniciar sesión'

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
    return redirect('/')


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


def jugar(request):
    # get_or_create obtiene el objeto de la base de datos o lo crea 
    QuizUser, created = QuizUsuario.objects.get_or_create(usuario=request.user)
    # Validar si la respuesta es verdadera o falsa y guardarla
    if request.method == 'POST':
        pregunta_pk = request.POST.get('pregunta_pk')
        pregunta_respondida = QuizUsuario.intentos.select_related('pregunta').get(pregunta__pk=pregunta_pk)
        respuesta_pk = request.POST.get('respuesta_pk')
    # Se renderizan las preguntas que no fueron respondidas
    else:
        respondidas = PreguntasRespondidas.objects.filter(quizUser=QuizUser).values_list('pregunta__pk', flat=True)
        pregunta = Pregunta.objects.exclude(pk__in=respondidas)
        context = {
            'pregunta': pregunta
        }
    return render(request, 'play/play.html', context)