from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .forms import RegistroFormulario, LoginFormulario

def inicio(request):
    context = {
        'bienvenidoValue': 'Bienvenido'
    }
    return render(request, 'inicio.html', context)


def userLogin(request):
    titulo='Iniciar sesión'

    form = LoginFormulario(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        usuario = authenticate(username=username, password=password)
        login(request, usuario)
        return redirect('/')
    
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