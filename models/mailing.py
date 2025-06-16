import logging
import markdown

from django.contrib import admin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

from beamz_website.models.blacklist import BlackList

_logger = logging.getLogger(__name__)


MAIL_TEMPLATES = {
    "basic": "Basic",
}

class Mailing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    planned = models.DateField()
    template = models.CharField(max_length=255, choices=MAIL_TEMPLATES, default='basic')
    message = models.TextField()

    def __str__(self):
        return self.title
    
    def _get_blacklist(self):
        return [b.email for b in BlackList.objects.all()]
    
    def _get_recipients(self):
        return [r.email for r in MailingRecipient.objects.filter(mailing=self)]
    
    def _add_emails(self, emails):
        bl = self._get_blacklist()
        existing_recipients = self._get_recipients()
        for email in emails:
            if email not in bl and email not in existing_recipients:
                MailingRecipient.objects.create(mailing=self, email=email)
                existing_recipients.append(email)

    def add_users(self):
        self._add_emails([usr.email for usr in User.objects.all()])

    def add_students(self):
        self._add_emails([usr.email for usr in User.objects.filter(profile__university__isnull=False)])

    def add_professionals(self):
        self._add_emails([usr.email for usr in User.objects.filter(profile__university__isnull=True)])
    
    def add_contacts(self):
        self._add_emails([contact.email for contact in Contact.objects.filter(active=True)])

    
class MailingRecipient(models.Model):
    id = models.AutoField(primary_key=True)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='recipients')
    email = models.EmailField()
    sent = models.BooleanField(default=False)

    def __str__(self):
        return str(self.mailing) + '-' + self.email
    
    def send_mailing(self):
        md = markdown.Markdown(extensions=["fenced_code"])
        msg = mark_safe(md.convert(self.mailing.message))
        html_message = render_to_string("mail/"+self.mailing.template+".html", {'message': msg, 'email': self.email})
        try:
            send_mail(self.mailing.title, strip_tags(html_message), None, [self.email], html_message=html_message)
        except Exception as e:
            _logger.error("Impossible to send email")
            _logger.error(e)
            return False
        self.sent = True
        self.save()
        _logger.info(f"Mailing sent to {self.email}")
        return True


class Contact(models.Model):
    email = models.EmailField(primary_key=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


@admin.action(description="Add all users to mailing")
def mailing_add_all_users(modeladmin, request, queryset):
    for rec in queryset:
        rec.add_users()

@admin.action(description="Add students to mailing")
def mailing_add_student_users(modeladmin, request, queryset):
    for rec in queryset:
        rec.add_students()

@admin.action(description="Add professional users to mailing")
def mailing_add_pro_users(modeladmin, request, queryset):
    for rec in queryset:
        rec.add_professionals()

@admin.action(description="Add contacts to mailing")
def mailing_add_contacts(modeladmin, request, queryset):
    for rec in queryset:
        rec.add_contacts()

