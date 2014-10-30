# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import ugettext_lazy as _
from datetime import date, timedelta


class EventManager(models.Manager):
    """Custom manager for ``Event`` model.

    The aim for the methods defined here are to provide shortcuts to get
    information about events.

    """
    def active(self, **kwargs):
        """Returns  an active events list."""
        return self.filter(is_active=True, **kwargs)

    def inactive(self, **kwargs):
        """Returns an inactive events list."""
        return self.filter(is_active=False, **kwargs)

    def get_recents(self, top=0, user=None, site=None, **kwargs):
        """Returns a recent events list sorted by creation date and a posibility to extract a top number from the list."""
        if not site:
            site = Site.objects.get_current()

        # if User is not given on parameters returns top five recent events
        limit = top if top > 0 else 5
        if not user:
            return self.active(site=site, **kwargs).order_by('-creation_date')[:limit]
        else:
            return self.active(site=site, user=user, **kwargs).order_by('-creation_date')[:limit]

    def get_by_site(self, site=None, **kwargs):
        """Returns events by site."""
        if not site:
            site = Site.objects.get_current()
        return self.filter(site=site, **kwargs)

    def get_by_user(self, user, site=None, **kwargs):
        """Returns all events filtered by user."""
        if not site:
            site = Site.objects.get_current()
        return self.active(user=user, site=site, **kwargs)

    def get_inactive_by_user(self, user, site=None, **kwargs):
        """Returns all inactive events filtered by user"""
        if not site:
            site = Site.objects.get_current()
        return self.inactive(user=user, site=site, **kwargs)

    def get_next_events(self, user=None, site=None, **kwargs):
        """Returns an events list with the next events."""
        if not site:
            site = Site.objects.get_current()
        if not user:
            return self.active(site=site, **kwargs).filter(eventdate__date__gte=date.today()).distinct()
        else:
            return self.active(user=user, site=site, **kwargs).filter(eventdate__date__gte=date.today()).distinct()

    def get_past_due(self, user=None, site=None, **kwargs):
        """Returns a list with the past due events."""
        if not site:
            site = Site.objects.get_current()
        if not user:
            return self.active(site=site, **kwargs).filter(eventdate__date__lt=date.today()).exclude(eventdate__date__gte=date.today()).distinct()
        else:
            return self.active(user=user, site=site, **kwargs).filter(eventdate__date__lt=date.today()).exclude(eventdate__date__gte=date.todat()).distinct()

    def get_today_events(self, user=None, site=None, **kwargs):
        """Returns a list with today events."""
        if not site:
            site = Site.objects.get_current()
        if not user:
            return self.active(site=site, **kwargs).filter(eventdate__date__iexact=date.today()).distinct()
        else:
            return self.active(user=user, site=site, **kwargs).filter(eventdate__date__iexact=date.today()).distinct()

    def get_by_date(self, date_event=None, user=None, site=None, **kwargs):
        """Returns an events list filtered by date."""
        if not site:
            site = Site.objects.get_current()

        if not user:
            return self.active(site=site, **kwargs).filter(eventdate__date=date_event).distinct()
        else:
            return self.active(user=user, site=site, **kwargs).filter(eventdate__date=date_event).distinct()

    def get_by_month(self, month=0, user=None, site=None, **kwargs):
        """Returns an events list filtered by Month."""
        if not site:
            site = Site.objects.get_current()
        searched_month = month if month > 0 else 1
        if not user:
            return self.active(site=site, **kwargs).filter(eventdate__date__month=searched_month).distinct()
        else:
            return self.active(user=user, site=site, **kwargs).filter(eventdate__date__month=searched_month).distinct()

    def get_this_week(self, user=None, site=None, **kwargs):
        """Returns an events list for this week.

          Take todays date. Subtract the number of days which already
          passed this week (this gets you 'last' monday). Add one week.
        """
        if not site:
            site = Site.objects.get_current()
        today = date.today()
        first_week_day = today - timedelta(days=today.weekday())
        print first_week_day
        last_week_day = today + timedelta(days=-today.weekday(), weeks=1)
        print last_week_day

        if not user:
            return self.active(site=site, **kwargs).filter(eventdate__date__range=(first_week_day, last_week_day)).distinct()
        else:
            return self.active(user=user, site=site, **kwargs).filter(eventdate__date__range=(first_week_day, last_week_day)).distinct()


class Event(models.Model):
    """Events Calendar."""
    site = models.ForeignKey(Site, verbose_name=_('Site'))
    user = models.ForeignKey(User, verbose_name=_('User'))
    title = models.CharField(_('Title event'), max_length=150, blank=False)
    slug = AutoSlugField(_('Slug'), max_length=150,
                         blank=False, unique=True,
                         help_text=_('This field is auto generated based on event title'),
                         populate_from='title')
    event_content = models.TextField(_('Event description'), blank=True)
    presentation_thumb = models.ImageField(_('Image presentation for events section'),
                                           upload_to='events/presentation-thumbs', max_length=150,
                                           help_text=_('You must define some standard zise for your events section'))
    creation_date = models.DateTimeField(_('Creation date'), auto_now_add=True,
                                         blank=True,
                                         null=True)
    last_update = models.DateTimeField(_('Last Update'), auto_now=True,
                                       blank=True, null=True)
    is_active = models.BooleanField(_('Is Active?'), default=True)
    objects = EventManager()

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events Calendar')
        ordering = ['creation_date']

    def __unicode__(self):
        return '%s' % (self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('event', (), {
            'slug': self.slug})

    def get_summary_dates(self):
        """Returns a summary of dates on this format: May (13, 20, 21)-Jun (1, 23, 30)."""
        from itertools import groupby
        from django.template.defaultfilters import date as _date
        event_dates = self.eventdate_set.all()
        list_item_dates = []
        for month, days in groupby(event_dates, lambda current_date: current_date.date.strftime("%B")):
            item_date = "%s (%s)" % (month, ",".join(list([str(day.date.day) for day in days])))
            list_item_dates.append(item_date)
        return "-".join(list_item_dates)

    def get_first_day(self):
        return self.eventdate_set.all().order_by('date')[0].date

    def get_last_day(self):
        return self.eventdate_set.all().order_by('-date')[0].date


class EventDate(models.Model):
    """Event Date"""
    CANCELLED = 'CANCELLED'
    ACTIVE = 'ACTIVE'
    SUSPENDED = 'SUSPENDED'
    DATE_STATUS_CHOICES = (
        (ACTIVE, _('Active')),
        (SUSPENDED, _('Suspended')),
        (CANCELLED, _('Cancelled')),
    )

    event = models.ForeignKey(Event, verbose_name=_('Event'))
    date = models.DateField(_('Date'), blank=False, null=False)
    time = models.TimeField(_('Time'), blank=True, null=True)
    country = models.CharField(_('Country'), max_length=100, blank=True)
    state = models.CharField(_('State'), max_length=100, blank=True)
    city = models.CharField(_('City'), max_length=100, blank=True)
    place = models.CharField(_('Place Event'), max_length=200, blank=True)
    status = models.CharField(_('Status Event date'), max_length=10, blank=False,
                              choices=DATE_STATUS_CHOICES, default=ACTIVE)
    aditional_comments = models.CharField(_('Aditional comments'), max_length=250, blank=True)

    class Meta:
        verbose_name = _('Event Date')
        verbose_name_plural = _('Dates and places for event')

    def __unicode__(self):
        return '%s-%s-%s' % (self.date, self.time, self.country)

    @models.permalink
    def get_absolute_url(self):
        return ('event_date', (), {
                'date': self.event_date, })


class ImageGallery(models.Model):
    """Image gallery for Event."""
    event = models.ForeignKey(Event, verbose_name=_('Event'))
    image_item = models.ImageField(_('Image item'), upload_to='events/gallery', max_length=150)
    description = models.CharField(_('Image description'), max_length=150, blank=True)

    class Meta:
        verbose_name = _('Image Event')
        verbose_name_plural = _('Image Gallery for event')

    def __unicode__(self):
        if self.description is not None:
            return '%s' % self.description
        else:
            return '%s' % str(self.image_item)


class VideoGallery(models.Model):
    """Video Gallery for Event"""
    event = models.ForeignKey(Event, verbose_name=_('Event'))
    video_item = models.CharField(_('Video Item'), max_length=400, blank=True)
    description = models.CharField(_('Video description'), max_length=150,
                                   blank=True)

    class Meta:
        verbose_name = _('Video Event')
        verbose_name_plural = _('Video Gallery for event')

    def __unicode__(self):
        if self.description is not None:
            return '%s' % self.description
        else:
            return '%s' % str(self.video_item)
