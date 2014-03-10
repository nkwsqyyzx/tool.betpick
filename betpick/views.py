from django.template.loader import get_template
from django.template import Template, Context
from django.http import HttpResponse

from tool.OddsProvider import OddsProvider

def odds(request,mid):
    oddslist = []
    rs = OddsProvider(mid).getResult()
    for r in rs:
        oddslist.append(r)

    c = Context({'oddslist': oddslist})
    t = get_template('oddslist.html')
    html = t.render(c)
    return HttpResponse(html)

def home(request):
    t = get_template('home.html')
    html = t.render(Context())
    return HttpResponse(html)
