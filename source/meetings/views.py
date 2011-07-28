
from django.shortcuts import render, get_object_or_404

from meetings.models import Guest


def guest_confirm(request):
    guest = get_object_or_404(Guest,
        fakeid=request.GET.get('f'),
        key=request.GET.get('k'))

    return render(request, 'meetings/guest_confirm.html',
        {
            'guest': guest,
        },
    )
