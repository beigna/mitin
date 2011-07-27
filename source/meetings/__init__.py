
from django.db.models.signals import post_save

from meetings.models import Guest
from meetings.signals_handlers import email_notify

post_save.connect(email_notify, sender=Guest)
