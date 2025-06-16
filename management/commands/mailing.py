from datetime import timedelta, timezone as tz

from django.core.management.base import BaseCommand
from django.utils import timezone

from beamz_website.models.mailing import MailingRecipient


class Command(BaseCommand):
    help = "Send planned mailings"

    def handle(self, *args, **options):
        to_send = MailingRecipient.objects.filter(
            mailing__planned__lte=timezone.now(),
            sent=False
        )
        for mail in to_send:
            try:
                if mail.send_mailing():
                    self.stdout.write(self.style.SUCCESS(f'Successfully sent email to {mail.email}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error sending email to {mail.email}: {e}'))
                continue
        self.stdout.write(self.style.SUCCESS('Successfully sent mailings'))
