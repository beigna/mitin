from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext as _

from django.contrib.auth.models import User


class Meeting(models.Model):
    owner = models.ForeignKey(User, blank=True, null=True)

    when = models.DateTimeField(_('When'))
    where = models.CharField(_('Where'), max_length=128)
    description = models.TextField(_('Description'))

    limited_seating = models.BooleanField(_('Limited seating'))
    min_guests = models.PositiveIntegerField(_('Min guests'), blank=True, null=True)
    max_guests = models.PositiveIntegerField(_('Max guests'), blank=True, null=True)
    allow_waitlist = models.BooleanField(_('Allow waitlist'))


    def __unicode__(self):
        label = self.description
        if len(label) > 15:
            label = '%s ...' % label[:15]
        return label

    def clean(self):
        if self.limited_seating:
            if self.max_guests < self.min_guests:
                raise ValidationError(_('Max guets must be greater than Min guest.'))


    class Meta:
        verbose_name = _('Meeting')
        verbose_name_plural = _('Meetings')


class Guest(models.Model):
    meeting = models.ForeignKey(Meeting)

    confirmation_code = models.CharField(max_length=128, unique=True)
    email = models.EmailField(_('Email'), unique=True)


