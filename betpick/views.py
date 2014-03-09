from django.template.loader import get_template
from django.template import Template, Context
from django.http import HttpResponse

def odds(request,mid):
    return HttpResponse("Hello world %s" % mid)

def home(request):
    t = get_template('home.html')
    html = t.render(Context())
    return HttpResponse(html)
