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
from datetime import datetime, timedelta
def nowscore_odds(request,mid):
    home = request.GET.get('home')
    guest = request.GET.get('guest')
    t = request.GET.get('t')
    if t:
        minutes = int(t.split(':')[0]) * 60 + int(t.split(':')[1])
        now = datetime.now()
        delta = minutes - now.hour * 60 - now.minute
        if delta <= 30:
            m = 5 * 60;
        elif delta <= 60:
            m = 10 * 60;
        elif delta < 120:
            m = 15 * 60;
        else:
            delta = 30 * 60;
    else:
        delta = 7 * 24 * 60 * 60;

    rs = NowScoreOddsProvider(mid,timeout=delta).getResult()
    oddslist = []
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

def nowscore_euro(request,mid):
    home = request.GET.get('home')
    guest = request.GET.get('guest')
    oddslist = []
    rs = NowScoreOddsProvider(mid).getResult(companyFilter = ['威廉希尔','立博','Bet365','SNAI','Inter wetten',])
    for r in rs.odds:
        oddslist.append(r)

    c = Context({'oddslist': oddslist,'home':home,'guest':guest})
    t = get_template('app_odds/templates/app_odds/euro.html')
    html = t.render(c)
    return HttpResponse(html)

from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
def nowscore_history(request):
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
    t = get_template('app_odds/templates/app_odds/nowscore_history.html')
    html = t.render(Context({'specified_date':date}))
    return HttpResponse(html)

def nowscore_next(request):
    page_number = request.GET.get('page_number')
    try:
        # 看看page_number数字是不是int
        page_number = int(page_number)
        if page_number > 7 or page_number < 1:
            page_number = 1
    except (ValueError,TypeError):
        page_number = 1
        return HttpResponseRedirect('/odds/nowscore/next/?page_number='+str(page_number))

    t = get_template('app_odds/templates/app_odds/nowscore_next.html')
    html = t.render(Context({'current_time':int(time.time())*1000,'page_number':page_number}))
    return HttpResponse(html)
