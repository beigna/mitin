
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from audits.models import Audit
from lib.hashes import salt, encrypt


class Meeting(Audit):
    class Meta:
        verbose_name = _('Meeting')
        verbose_name_plural = _('Meetings')

    owner = models.ForeignKey(User, blank=True, null=True)
    owner_email = models.EmailField()

    fakeid = models.CharField(max_length=40, unique=True)
    salt = models.CharField(max_length=40, unique=True)
    key = models.CharField(max_length=40, unique=True)

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

    is_confirmed = models.BooleanField(_('Is confirmed?'))


    def __unicode__(self):
        label = self.description
        if len(label) > 15:
            label = u'%s ...' % label[:15]
        return label

    def clean(self):
        if self.limited_seating:
            if self.max_guests < self.min_guests:
                raise ValidationError(_('Max guets must be greater than Min guest.'))

    def save(self, *args, **kwargs):
        if not self.pk:
            self.salt = salt()
            self.key = encrypt(phrase=self.owner_email, salt=self.salt)
            self.fakeid = encrypt(phrase=self.key, salt=self.salt)

        super(Meeting, self).save(*args, **kwargs)


class Guest(Audit):
    class Meta:
        unique_together = ('meeting', 'email')
        verbose_name = _('Guest')
        verbose_name_plural = _('Guests')

    ATTENDING_CHOICES = (
        ('yes', _('Yes')),
        ('no', _('No')),
        ('maybe', _('May be')),
    )

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
            self.salt = salt()
            self.key = encrypt(phrase=self.email, salt=self.salt)
            self.fakeid = encrypt(phrase=self.key, salt=self.salt)

        super(Guest, self).save(*args, **kwargs)
