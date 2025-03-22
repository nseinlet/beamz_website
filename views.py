from django.shortcuts import render
from django.db.models import Q
from .models.faq import Faq, FaqSection

def index(request):
    context = {}
    return render(request, 'webindex.html', context)

def features(request):
    context = {}
    return render(request, 'features.html', context)

def pricing(request):
    context = {}
    return render(request, 'pricing.html', context)

def aboutus(request):
    context = {}
    return render(request, 'aboutus.html', context)

def faq(request):
    context = {}
    fqc = FaqSection.objects.filter(Q(active=True))
    context['faq_sections'] = []
    for section in fqc:
        faqs = Faq.objects.filter(Q(active=True) & Q(section_id=section))
        qr = [{'question': faq.question, 'answer': faq.answer, 'short_answer': faq.short_answer} for faq in faqs]
        context['faq_sections'].append({'section': section, 'qr': qr})
    
    return render(request, 'faq.html', context)
