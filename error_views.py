import random

from django.shortcuts import render


def error_400(request, exception=None):
    img = random.randint(1, 3)
    return render(request, 'error.html', context={'img': img, 'code': 400}, status=400)

def error_403(request, exception=None):
    img = random.randint(1, 3)
    return render(request, 'error.html', context={'img': img, 'code': 403}, status=403)

def error_404(request, exception=None):
    img = random.randint(1, 3)
    return render(request, 'error.html', context={'img': img, 'code': 404}, status=404)

def error_500(request, exception=None):
    img = random.randint(1, 4)
    return render(request, 'error.html', context={'img': img, 'code': 500}, status=500)
