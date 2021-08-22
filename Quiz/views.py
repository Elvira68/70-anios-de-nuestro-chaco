from django.shortcuts import render

def inicio(request):
    context = {
        'bienvenidoValue': 'Bienvenido'
    }
    return render(request, 'inicio.html', context)