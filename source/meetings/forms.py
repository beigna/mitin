
from django import forms

from meetings.models import Meeting, Guest


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        exclude = ('owner', 'key', 'salt', 'fakeid', 'is_confirmed')


class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        exclude = ('fakeid', 'salt', 'key', 'attending',
            'is_responded')


class GuestRespondForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ('attending',)
