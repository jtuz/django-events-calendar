# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from models import Event
from json import JsonResponse

def fullcalendar_data(request):
    """Json String for fullcalendar jquery plugin (http://arshaw.com/fullcalendar/)."""
    # FIXME: Acentos en los titulos
    data_aux = [{
              "title":item.title,
              "start": str(item.get_first_day()),
              "end": str(item.get_last_day()),
              "url": item.get_absolute_url(),
              }
            for item in Event.objects.active()]
    return JsonResponse(data_aux)


def event(request, slug):
    """Return an event."""
    item = get_object_or_404(Event, slug=slug, is_active=True)
    ctx = RequestContext(request, {'item': item})
    return render_to_response('events/event.html', context_instance=ctx)
