from datetime import datetime

from django.shortcuts import render
from django.db.models import Q

from .models.faq import Faq, FaqSection
from .models.blog import BlogPost, BlogTag
from beamz.models import University


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
    fqc = FaqSection.objects.filter(Q(active=True)).order_by('order')
    context['faq_sections'] = []
    for section in fqc:
        faqs = Faq.objects.filter(active=True, section_id=section).order_by('order')
        context['faq_sections'].append({'section': section, 'qr': faqs})
    return render(request, 'faq.html', context)

def blog(request, tag=None, year=None, month=None):
    blogs = BlogPost.objects.filter(published=True, publication_date__lte=datetime.now())
    if tag:
        blogs = blogs.filter(tags__name=tag)
    elif year and month:
        blogs = blogs.filter(publication_date__year=year, publication_date__month=month)
    blogs = blogs.order_by('-publication_date', 'id')
    the_dates = BlogPost().get_dates_context()
    context = {
        'blog_tags': BlogTag.objects.filter(active=True).order_by('order', 'name'),
        'blogs': blogs,
        'pub_dates':the_dates,
    }
    return render(request, 'blog.html', context)

def blog_post(request, post_id, title=''):
    context = {}
    try:
        blog = BlogPost.objects.get(id=post_id)
        context['blog'] = blog
        context['blog_tags'] = BlogTag.objects.filter(active=True).order_by('order', 'name')
        context['pub_dates'] = BlogPost().get_dates_context()
    except BlogPost.DoesNotExist:
        context['error'] = "Blog post not found."
    return render(request, 'blogpost.html', context)

def universities(request):
    context = {'universities': University.objects.filter(published=True).order_by('name')}
    return render(request, 'universities.html', context)