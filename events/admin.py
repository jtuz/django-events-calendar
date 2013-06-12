# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf import settings
from django.utils.translation import ungettext, ugettext_lazy as _
from events.models import Event, EventDate, ImageGallery, VideoGallery
from widgets import AdminImageWidget, AdminYoutubeWidget


class EventDateInline(admin.TabularInline):
    model = EventDate
    fieldsets = (
        (_('Dates and places for event'), {
            'classes': ('collapse',),
            'fields': ('date',
                       'time',
                       'country',
                       'state',
                       'city',
                       'place',
                       'status',
                       'aditional_comments', )
        }),
    )
    extra = 3


class ImageGalleryInline(admin.TabularInline):
    fieldsets = (
        (_('Image Gallery'), {
            'classes': ('collapse',),
            'fields': ('image_item', 'description', )
        }),
    )
    model = ImageGallery
    extra = 3

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'image_item':
            kwargs.pop("request", None)
            kwargs['widget'] = AdminImageWidget
            return db_field.formfield(**kwargs)
        return super(ImageGalleryInline, self).formfield_for_dbfield(db_field, **kwargs)


class VideoGalleryInline(admin.TabularInline):
    model = VideoGallery
    extra = 3

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'video_item':
            kwargs.pop("request", None)
            kwargs['widget'] = AdminYoutubeWidget
            return db_field.formfield(**kwargs)
        return super(VideoGalleryInline, self).formfield_for_dbfield(db_field, **kwargs)


class EventAdmin(admin.ModelAdmin):
    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/static/')
        js = (static_url+'js/tinymce/tinymce.min.js',
              static_url+'js/textarea-events.js')

    inlines = [EventDateInline, ImageGalleryInline, VideoGalleryInline]
    list_display = ['user', 'title', 'creation_date', 'last_update', 'is_active']
    list_display_links = ['title']
    list_filter = ['is_active', 'site']
    search_fields = ['title']
    exclude = ['user']
    actions = ['active_events', 'deactivate_events']

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'presentation_thumb':
            kwargs.pop("request", None)
            kwargs['widget'] = AdminImageWidget
            return db_field.formfield(**kwargs)
        return super(EventAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def save_model(self, request, obj, form, change):
        """Sets current user (logged in) as Event editor."""
        obj.user = request.user
        obj.save()

    def queryset(self, request):
        """Filter events by current user(logged in)."""
        qs = super(EventAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def active_events(self, request, queryset):
        """Marks the selected events as published."""
        row_count = queryset.update(is_active=True)
        message_bit = ungettext('%(row_count)d Event was successfully marked as published',
                                '%(row_count)d Events were successfully marked as published', row_count) % {'row_count': row_count}
        self.message_user(request, '%(message_bit)s' % {'message_bit': message_bit})

    active_events.short_description = _('Publish')

    def deactivate_events(self, request, queryset):
        """Marks the selected events as not published."""
        row_count = queryset.update(is_active=False)
        message_bit = ungettext('%(row_count)d Event was successfully marked as not published',
                                '%(row_count)d Events were successfully marked as not published', row_count) % {'row_count': row_count}
        self.message_user(request, '%(message_bit)s' % {'message_bit': message_bit})

    deactivate_events.short_description = _('Deactivate publication')


admin.site.register(Event, EventAdmin)
