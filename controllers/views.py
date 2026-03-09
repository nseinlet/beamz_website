from datetime import datetime

from django.shortcuts import render
from django.db.models import Q, Max
from django.core.mail import send_mail, BadHeaderError
from django.http import JsonResponse
from django.conf import settings

from ..forms import ContactUsForm
from ..models.faq import Faq, FaqSection
from ..models.blog import BlogPost, BlogTag
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

def contactus(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            # Récupération des champs
            fullname = form.cleaned_data['fullname']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Corps du mail
            body = f"""
            Nom : {fullname}
            Email : {email}

            Message :
            {message}
            """

            try:
                send_mail("Contact web", body, None, [m[1] for m in settings.ADMINS])
                return JsonResponse({"success": True, "message": "Votre message a été envoyé."})
            except BadHeaderError:
                return JsonResponse({"success": False, "message": "Erreur d'entête dans l'email."})
    else:
        form = ContactUsForm()
    return render(request, "contactus.html", {"form": form})


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

def sitemap(request):
    blog_last_mod = BlogPost.objects.filter(published=True).aggregate(Max("publication_date", default='2025-01-01'))
    faq_last_mod = Faq.objects.aggregate(Max("created_at", default='2025-01-01'))
    sitemap_urls = [
        {'location': 'https://beamze.app/', 'priority': '1.0', 'lastmod': '2026-01-01', 'changefreq': 'monthly'},
    ]
    for lang in ['en', 'fr']:
        sitemap_urls.append({'location': f'https://beamze.app/{lang}/', 'priority': '1.0', 'lastmod': '2026-01-01', 'changefreq': 'monthly'})
        sitemap_urls.append({'location': f'https://beamze.app/{lang}/faq', 'priority': '0.7', 'lastmod': faq_last_mod['created_at__max'].strftime('%Y-%m-%d'), 'changefreq': 'monthly'})
        sitemap_urls.append({'location': f'https://beamze.app/{lang}/pricing', 'priority': '0.8', 'lastmod': '2026-01-01', 'changefreq': 'yearly'})
        sitemap_urls.append({'location': f'https://beamze.app/{lang}/features', 'priority': '0.8', 'lastmod': '2026-01-01', 'changefreq': 'monthly'})
        sitemap_urls.append({'location': f'https://beamze.app/{lang}/features/static', 'priority': '0.7', 'lastmod': '2026-02-20', 'changefreq': 'yearly'})
        sitemap_urls.append({'location': f'https://beamze.app/{lang}/features/second_order', 'priority': '0.7', 'lastmod': '2026-03-01', 'changefreq': 'yearly'})
        sitemap_urls.append({'location': f'https://beamze.app/{lang}/aboutus', 'priority': '0.6', 'lastmod': '2026-01-01', 'changefreq': 'yearly'})
        sitemap_urls.append({'location': f'https://beamze.app/{lang}/contactus', 'priority': '0.6', 'lastmod': '2026-01-01', 'changefreq': 'yearly'})
        sitemap_urls.append({'location': f'https://beamze.app/{lang}/universities', 'priority': '0.5',  'lastmod': '2025-09-01',  'changefreq': 'yearly'})
        sitemap_urls.append({'location': f'https://beamze.app/{lang}/blog', 'priority': '0.7', 'lastmod': blog_last_mod['publication_date__max'].strftime('%Y-%m-%d'), 'changefreq': 'weekly'})
    for tag in BlogTag.objects.filter(active=True):
        sitemap_urls.append({'location': f'https://beamze.app/blog/tag/{tag.name}/', 'priority': '0.6', 'lastmod': tag.created_at.strftime('%Y-%m-%d'), 'changefreq': 'yearly'})
        sitemap_urls.append({'location': f'https://beamze.app/en/blog/tag/{tag.name}/', 'priority': '0.6', 'lastmod': tag.created_at.strftime('%Y-%m-%d'), 'changefreq': 'yearly'})
        sitemap_urls.append({'location': f'https://beamze.app/fr/blog/tag/{tag.name_fr}/', 'priority': '0.6', 'lastmod': tag.created_at.strftime('%Y-%m-%d'), 'changefreq': 'yearly'})
    for dt in BlogPost().get_dates_context():
        year = dt['year']
        for month in dt['month']:
            m = month['m']
            sitemap_urls.append({'location': f'https://beamze.app/blog/month/{year}/{m}/', 'priority': '0.6', 'lastmod': f'{year}-{m}-28', 'changefreq': 'yearly'})
            sitemap_urls.append({'location': f'https://beamze.app/en/blog/month/{year}/{m}/', 'priority': '0.6', 'lastmod': f'{year}-{m}-28', 'changefreq': 'yearly'})
            sitemap_urls.append({'location': f'https://beamze.app/fr/blog/month/{year}/{m}/', 'priority': '0.6', 'lastmod': f'{year}-{m}-28', 'changefreq': 'yearly'})
    for blog in BlogPost.objects.filter(published=True):
        sitemap_urls.append({'location': f'https://beamze.app/blog/{blog.get_slug()}/', 'priority': '0.5', 'lastmod': blog.publication_date.strftime('%Y-%m-%d'), 'changefreq': 'yearly'})
        sitemap_urls.append({'location': f'https://beamze.app/en/blog/{blog.get_slug()}/', 'priority': '0.5', 'lastmod': blog.publication_date.strftime('%Y-%m-%d'), 'changefreq': 'yearly'})
        sitemap_urls.append({'location': f'https://beamze.app/fr/blog/{blog.get_slug('fr')}/', 'priority': '0.5', 'lastmod': blog.publication_date.strftime('%Y-%m-%d'), 'changefreq': 'yearly'})
    context = {
        'sitemap_urls': sitemap_urls,
    }
    return render(request, 'sitemap.html', context)