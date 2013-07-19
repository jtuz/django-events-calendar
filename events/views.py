from models import Event

def fullcalendar_data(request, slug):
    """Json String for fullcalendar jquery plugin (http://arshaw.com/fullcalendar/)."""
    from django.http import HttpResponse
    from django.utils import simplejson
    #FIXME: Acentos en los titulos
    data_aux = [{
              "title":item.title, 
              "start": str(item.get_first_day()), 
              "end": str(item.get_last_day()), 
              "url": item.get_absolute_url(),
              }
            for item in Event.objects.active()]
    return HttpResponse(simplejson.dumps(data_aux), mimetype='application/json')
