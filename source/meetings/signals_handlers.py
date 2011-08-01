
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def email_owner_notify(sender, **kwargs):
    meeting = kwargs['instance']

    if not meeting.is_confirmed:
        subject = u'Confirma tu evento'
        message = render_to_string('emails/confirm.html', {'meeting': meeting})

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_SENDER,
            recipient_list=[meeting.owner_email]
        )

def email_guest_notify(sender, **kwargs):
    guest = kwargs['instance']

    subject = u'Te invitaron a %s' % guest.meeting.where
    message = render_to_string('emails/respond.html', {'guest': guest})

    send_mail(subject=subject, message=message,
        from_email=settings.EMAIL_SENDER, recipient_list=[guest.email])
