from django.contrib import admin

from meetings.models import Meeting, Guest


class MeetingAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', 'key', 'salt', 'fakeid',
        'created_at', 'updated_at')


class GuestAdmin(admin.ModelAdmin):
    list_display = ('meeting', 'email', 'attending', 'is_responded')
    readonly_fields = ('key', 'salt', 'fakeid', 'created_at', 'updated_at')

admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Guest, GuestAdmin)
