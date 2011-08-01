
from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _

from audits.models import Audit
from lib.hashes import salt, encrypt


class Meeting(Audit):
    class Meta:
        verbose_name = _('Meeting')
        verbose_name_plural = _('Meetings')

    owner = models.ForeignKey(User, blank=True, null=True)
    owner_email = models.EmailField()

    title = models.CharField(_('Title'), max_length=40)
    slug = models.CharField(max_length=50, unique=True, editable=False)
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

    # for secure confirm
    fakeid = models.CharField(max_length=40, unique=True)
    salt = models.CharField(max_length=40, unique=True)
    key = models.CharField(max_length=40, unique=True)

    def __unicode__(self):
        return u'%s' % self.title

    def clean(self):
        if self.limited_seating:
            if self.max_guests < self.min_guests:
                raise ValidationError(_('Max guets must be greater than Min guest.'))

    def save(self, *args, **kwargs):
        if not self.pk:
            self.salt = salt()
            self.key = encrypt(phrase=self.owner_email, salt=self.salt)
            self.fakeid = encrypt(phrase=self.key, salt=self.salt)

            self.slug = slugify('%s-%s' % (self.when.strftime('%y%m%d%H%M'),
                self.title))

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

    name = models.CharField(_('Name'), max_length=50, blank=True, null=True)
    email = models.EmailField(_('Email'))

    attending = models.CharField(_('Attending'), max_length=10,
        choices=ATTENDING_CHOICES, blank=True, null=True, db_index=True)
    is_responded = models.BooleanField(_('Is responded?'))

    # for secure respond
    fakeid = models.CharField(max_length=40, unique=True)
    salt = models.CharField(max_length=40, unique=True)
    key = models.CharField(max_length=40, unique=True)

    def __unicode__(self):
        return u'%s <%s>' % (self.name, self.email)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.salt = salt()
            self.key = encrypt(phrase=self.email, salt=self.salt)
            self.fakeid = encrypt(phrase=self.key, salt=self.salt)

        super(Guest, self).save(*args, **kwargs)
