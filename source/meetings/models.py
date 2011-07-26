from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Meeting(models.Model):
    owner = models.ForeignKey(User, blank=True, null=True)

    when = models.DateTimeField()
    where = models.CharField(max_length=128)
    description = models.TextField()

    limited_seating = models.BooleanField()
    max_guests = models.PositiveIntegerField(blank=True, null=True)
    min_guests = models.PositiveIntegerField(blank=True, null=True)
    allow_waitlist = models.BooleanField()

    def __unicode__(self):
        txt = self.description
        if len(txt) > 15:
            txt = '%s ...' % txt[:15]
        return txt
