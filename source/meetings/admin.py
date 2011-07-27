from django.contrib import admin

from meetings.models import Meeting, Guest


class MeetingAdmin(admin.ModelAdmin):
    pass


class GuestAdmin(admin.ModelAdmin):
    list_display = ('meeting', 'email', 'attending', 'is_responded')
    readonly_fields = ('key', 'salt', 'fakeid')

admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Guest, GuestAdmin)
