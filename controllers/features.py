from django.shortcuts import render
from django.utils.translation import get_language

def static(request):
    lang = get_language()
    if lang == 'fr':
        return render(request, 'features/static_fr.html', {})
    return render(request, 'features/static.html', {})

def second_order(request):
    lang = get_language()
    if lang == 'fr':
        return render(request, 'features/secondorder_fr.html', {})
    return render(request, 'features/secondorder.html', {})