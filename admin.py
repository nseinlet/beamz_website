from django.db import models
from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from .models.blog import BlogTag, BlogPost, BlogPicture
from .models.faq import FaqSection, Faq
from .models.blacklist import BlackList
from .models.mailing import Mailing, MailingRecipient, mailing_add_all_users, mailing_add_student_users, mailing_add_pro_users, Contact

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

@admin.register(BlackList)
class BlackListAdmin(admin.ModelAdmin):
    list_display = [ 'email', 'created_at' ]

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = [ 'title', 'planned', 'template' ]
    actions = [ mailing_add_all_users, mailing_add_student_users, mailing_add_pro_users ]

@admin.register(MailingRecipient)
class MailingRecipientAdmin(admin.ModelAdmin):
    list_display = [ 'mailing', 'email', 'sent' ]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = [ 'email', 'active' ]
