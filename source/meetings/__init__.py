
from django.db.models.signals import post_save

from meetings.models import Meeting, Guest
from meetings.signals_handlers import email_owner_notify, email_guest_notify

post_save.connect(email_guest_notify, sender=Guest)
post_save.connect(email_owner_notify, sender=Meeting)
