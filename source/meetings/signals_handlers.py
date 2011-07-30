
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def email_notify(sender, **kwargs):
    guest = kwargs['instance']

    subject = u'Te invitaron a %s' % guest.meeting.where
    message = render_to_string('emails/guest_confirm.html', {'guest': guest})

    send_mail(subject=subject, message=message,
        from_email=settings.EMAIL_SENDER, recipient_list=[guest.email])
