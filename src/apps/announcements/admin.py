from django.contrib import admin
from .models import Announcement, Category, Attachment, Event


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "priority", "publish_date", "is_published")
    list_filter = ("category", "priority", "is_published", "publish_date")
    search_fields = ("title", "description")
    inlines = [AttachmentInline]


admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Category)


class EventAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "visible_to_students",
        "visible_to_parents",
        "visible_to_teachers",
        "starttime",
        "endtime",
        "date",
        "location",
    ]


admin.site.register(Event, EventAdmin)
