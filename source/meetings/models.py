
from hashlib import sha1
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from audits.models import Audit


class Meeting(Audit):
    owner = models.ForeignKey(User, blank=True, null=True)
    owner_email = models.EmailField()

    slug = models.CharField(max_length=50, unique=True)

    when = models.DateTimeField(_('When'))
    where = models.CharField(_('Where'), max_length=128)
    description = models.TextField(_('Description'))

    limited_seating = models.BooleanField(_('Limited seating'))
    min_guests = models.PositiveIntegerField(_('Min guests'),
        blank=True, null=True)
    max_guests = models.PositiveIntegerField(_('Max guests'),
        blank=True, null=True)
    allow_waitlist = models.BooleanField(_('Allow waitlist'))

    is_active = models.BooleanField(_('Is active?'))


    def __unicode__(self):
        label = self.description
        if len(label) > 15:
            label = u'%s ...' % label[:15]
        return label

    def clean(self):
        if self.limited_seating:
            if self.max_guests < self.min_guests:
                raise ValidationError(_('Max guets must be greater than Min guest.'))


    class Meta:
        verbose_name = _('Meeting')
        verbose_name_plural = _('Meetings')


class Guest(Audit):
    ATTENDING_CHOICES = (
        ('yes', _('Yes')),
        ('no', _('No')),
        ('maybe', _('May be')),
    )

    class Meta:
        unique_together = ('meeting', 'email')

    meeting = models.ForeignKey(Meeting)

    fakeid = models.CharField(max_length=40, unique=True)
    email = models.EmailField(_('Email'))
    salt = models.CharField(max_length=40, unique=True)
    key = models.CharField(max_length=40, unique=True)

    attending = models.CharField(_('Attending'), max_length=10,
        choices=ATTENDING_CHOICES, blank=True, null=True, db_index=True)
    is_responded = models.BooleanField(_('Is responded?'))

    def __unicode__(self):
        return u'%s' % self.email

    def save(self, *args, **kwargs):
        if not self.pk:
            self.salt = sha1('%s%s' % (datetime.now(), self.email)).hexdigest()
            self.key = sha1('%s%s' % (self.salt, self.email)).hexdigest()
            self.fakeid = sha1('%s%s' % (self.salt, self.key)).hexdigest()

        super(Guest, self).save(*args, **kwargs)
