
from django.shortcuts import render, get_object_or_404

from meetings.models import Guest
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
    guest = get_object_or_404(Guest,
        fakeid=request.GET.get('f'),
        key=request.GET.get('k'))

    return render(request, 'meetings/confirm.html',
        {
            'guest': guest,
        },
    )
