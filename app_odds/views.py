from django.http import HttpResponse
from django.shortcuts import render
from django.template import Template, Context
from django.template.loader import get_template

# Create your views here.
from app_odds.tool.OddsProvider import OddsProvider
def odds(request,mid):
    oddslist = []
    rs = OddsProvider(mid).getResult()
    for r in rs:
        oddslist.append(r)

    c = Context({'oddslist': oddslist})
    t = get_template('app_odds/templates/app_odds/oddslist.html')
    html = t.render(c)
    return HttpResponse(html)

def home(request):
    t = get_template('app_odds/templates/app_odds/home.html')
    html = t.render(Context())
    return HttpResponse(html)

from app_odds.tool.NowScoreOddsProvider import NowScoreOddsProvider
def nowscore(request,mid):
    home = request.GET.get('home')
    guest = request.GET.get('guest')
    oddslist = []
    rs = NowScoreOddsProvider(mid).getResult()
    for r in rs.odds:
        oddslist.append(r)

    c = Context({'oddslist': oddslist,'home':home,'guest':guest})
    t = get_template('app_odds/templates/app_odds/oddslist.html')
    html = t.render(c)
    return HttpResponse(html)

import time
def nowscore_home(request):
    t = get_template('app_odds/templates/app_odds/nowscore_home.html')
    html = t.render(Context({'current_time':int(time.time())*1000}))
    return HttpResponse(html)
