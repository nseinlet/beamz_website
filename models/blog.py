from datetime import datetime

from django.db import models
from django.db.models import Count
from django.utils.timezone import now
from django.db.models.functions import TruncMonth, TruncYear


class BlogTag(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    name_fr = models.CharField(max_length=200)
    order = models.IntegerField(default=10)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    id = models.BigAutoField(primary_key=True)
    published = models.BooleanField(default=False)
    publication_date = models.DateField(default=now, editable=True)
    tags = models.ManyToManyField(BlogTag, blank=True, related_name='blogs')
    title = models.CharField(max_length=250)
    title_fr = models.CharField(max_length=250, blank=True)
    description = models.TextField(help_text="Short description of the blog post")
    description_fr = models.TextField(blank=True)
    content = models.TextField(help_text="Full content of the blog post")
    content_fr = models.TextField(blank=True)
    blog_img = models.ImageField(upload_to='blog/articles/', blank=True)

    def __str__(self):
        return self.title

    def get_dates_context(self):
        pb_dates = BlogPost.objects.filter(published=True, publication_date__lte=datetime.now()).annotate(month=TruncMonth('publication_date')).values('month').annotate(nbr=Count("id")).distinct()
        list_dates = [(dt['month'].strftime("%Y"), dt['month'].strftime("%m"), dt['nbr']) for dt in pb_dates]
        pub_dates = {}
        for dt in list_dates:
            if not pub_dates.get(dt[0]):
                pub_dates[dt[0]] = {}
            pub_dates[dt[0]][dt[1]] = dt[2]
        the_dates = [
            {
                'year': year,
                'month': [
                    {'m': month, 'qty': pub_dates[year][month]}
                    for month in pub_dates[year]
                ]
            }
            for year in pub_dates
        ]

        # Sort in reverse order
        for year in the_dates:
            year['month'].sort(key=lambda x: (x['m']), reverse=True)
        the_dates.sort(key=lambda x: (x['year']), reverse=True)

        return the_dates
        