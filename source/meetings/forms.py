
from django import forms

from meetings.models import Meeting


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        exclude = ('owner',)
