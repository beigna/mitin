from django.contrib import admin

from meetings.models import Meeting


class MeetingAdmin(admin.ModelAdmin):
    pass

admin.site.register(Meeting, MeetingAdmin)
