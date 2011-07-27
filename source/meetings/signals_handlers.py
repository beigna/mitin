
from django.conf import settings
from django.core.mail import send_mail


def email_notify(sender, **kwargs):
    guest = kwargs['instance']

    url = 'http://localhost/fake_resource/'

    subject = u'Te invitaron a %s' % guest.meeting.where
    message = u'El %s en %s:\n%s\n\n%s?f=%s&k=%s' % (guest.meeting.when,
        guest.meeting.where, guest.meeting.description, url,
        guest.fakeid, guest.key)

    send_mail(subject=subject, message=message,
        from_email=settings.EMAIL_SENDER, recipient_list=[guest.email])
