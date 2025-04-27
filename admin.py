from django.db import models
from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from .models.blog import BlogTag, BlogPost, BlogPicture
from .models.faq import FaqSection, Faq


admin.site.register(BlogPicture)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = [ 'title', 'published', 'publication_date' ]
    fields = (('title', 'title_fr'), ('published', 'publication_date'), ('description', 'description_fr'), ('content', 'content_fr'), 'blog_img', 'tags' )
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'order', 'active' ]
    fields = (('name', 'name_fr'), ('order', 'active'))

@admin.register(FaqSection)
class FaqSectionAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'order', 'active' ]
    fields = [ ('name', 'name_fr'), ('active', 'order') ]

@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = [ 'section_id', 'order', 'active', 'question' ]
    fields = [ 'section_id', ('order', 'active'), ('question', 'question_fr'), ('short_answer', 'short_answer_fr'), ('answer', 'answer_fr') ]
