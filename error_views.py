import random

from django.shortcuts import render


def error_403(request, exception=None):
    img = random.randint(1, 3)
    return render(request, 'errors/403.html')

def error_404(request, exception=None):
    img = random.randint(1, 5)
    return render(request, 'errors/404.html')

def error_500(request, exception=None):
    img = random.randint(1, 4)
    return render(request, 'errors/500.html', context={'img': img})
