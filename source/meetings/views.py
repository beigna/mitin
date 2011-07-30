
from django.shortcuts import render, get_object_or_404

from meetings.models import Meeting, Guest
from meetings.forms import MeetingForm


def create(request):
    if request.method == 'GET':
        form = MeetingForm()

    return render(request, 'meetings/create.html',
        {
            'form': form,
        },
    )


def confirm(request):
    meeting = get_object_or_404(Meeting,
        fakeid=request.GET.get('f'),
        key=request.GET.get('k'))

    return render(request, 'meetings/confirm.html',
        {
            'meeting': meeting,
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
