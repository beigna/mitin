
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory

from meetings.models import Meeting, Guest
from meetings.forms import MeetingForm, GuestForm


def list(request):
    return render(request, 'meetings/list.html',
        {},
    )

def create(request):
    if request.method == 'GET':
        form = MeetingForm()

    elif request.method == 'POST':
        form = MeetingForm(instance=Meeting(), data=request.POST)

        if form.is_valid():
            new_meeting = form.save()
            return redirect(reverse('meetings_list'))


    return render(request, 'meetings/create.html',
        {
            'form': form,
        },
    )


def confirm(request):
    meeting = get_object_or_404(Meeting,
        fakeid=request.GET.get('f'),
        key=request.GET.get('k'))


    if request.method == 'GET':
        form = MeetingForm(instance=meeting)
        GuestFormSet = formset_factory(GuestForm, extra=5)
        guest_forms = GuestFormSet()

    elif request.method == 'POST':
        form = MeetingForm(instance=meeting, data=request.POST)
        GuestFormSet = formset_factory(GuestForm)
        guest_forms = GuestFormSet(request.POST)

        for gf in guest_forms:
            print gf.fields
            break


    return render(request, 'meetings/confirm.html',
        {
            'meeting': meeting,
            'form': form,
            'guest_forms': guest_forms,
        },
    )

def respond(request):
    guest = get_object_or_404(Guest,
        fakeid=request.GET.get('f'),
        key=request.GET.get('k'))

    return render(request, 'meetings/respond.html',
        {
            'guest': guest,
        },
    )
