
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory

from meetings.models import Meeting, Guest
from meetings.forms import MeetingForm, GuestForm


def list(request):
    meetings = Meeting.objects.all()

    return render(request, 'meetings/list.html',
        {
            'meetings': meetings,
        },
    )

def view(request, slug):
    meeting = get_object_or_404(Meeting, slug=slug)

    return render(request, 'meetings/view.html',
        {
            'meeting': meeting,
        },
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

def update(request, slug):
    raise NotImplemented()

def delete(request, slug):
    raise NotImplemented()

def confirm(request):
    meeting = get_object_or_404(Meeting,
        fakeid=request.GET.get('f'),
        key=request.GET.get('k'))

    if meeting.is_confirmed:
        return redirect(reverse('meetings_list'))

    if request.method == 'GET':
        form = MeetingForm(instance=meeting)
        GuestFormSet = modelformset_factory(Guest, fields=('email',), extra=5)
        guest_forms = GuestFormSet()

    elif request.method == 'POST':
        form = MeetingForm(instance=meeting, data=request.POST)
        GuestFormSet = modelformset_factory(Guest, fields=('email',))
        guest_forms = GuestFormSet(request.POST)

        if form.is_valid() and guest_forms.is_valid():
            form.save()
            instances = guest_forms.save(commit=False)

            for instance in instances:
                instance.meeting = meeting
                instance.save()

            return redirect(reverse('meetings_list'))

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
