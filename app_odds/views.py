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
def nowscore_odds(request,mid):
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


from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
def nowscore_history(request):
    t = get_template('app_odds/templates/app_odds/nowscore_history.html')
    passed = request.GET.get('passed')
    try:
        # 看看passed数字是不是int
        passed = int(passed)
        if passed > 365 or passed < 1:
            passed = 1
    except (ValueError,TypeError):
        passed = 1
        return HttpResponseRedirect('/odds/nowscore/history/?passed='+str(passed))
    date = (datetime.now() - timedelta(days=passed)).strftime('%Y/%m/%d')
    html = t.render(Context({'specified_date':date}))
    return HttpResponse(html)
