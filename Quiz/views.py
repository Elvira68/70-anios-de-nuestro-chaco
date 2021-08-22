from django.shortcuts import redirect, render
from .forms import RegistroFormulario

def inicio(request):
    context = {
        'bienvenidoValue': 'Bienvenido'
    }
    return render(request, 'inicio.html', context)

def registro(request):
    titulo = 'Crear una cuenta'

    if request.method == 'POST':
        form = RegistroFormulario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
    else:
        form = RegistroFormulario()
    
    context = {
        'form': form,
        'titulo': titulo
    }

    return render(request, 'usuario/registro.html', context)