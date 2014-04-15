from django.http import HttpResponse
from django.shortcuts import render
from django.template import Template, Context
from django.template.loader import get_template

# Create your views here.
from app_stat.tool import StatProvider
def stat_home(request):
    home,away,link = StatProvider.GetMatchesLink(leagueId=0)[0]
    homeMatches,awayMatches = StatProvider.GetMatchesByLink(link=link)
    context = []
    for matchid in homeMatches:
        t,h,a = StatProvider.GetStatics(matchid=matchid)
        context.append((t,h,a))
    c = Context({'stats': context})
    t = get_template('app_stat/templates/app_stat/home.html')
    html = t.render(c)
    return HttpResponse(html)

def stat_match(mid):
    return HttpResponse(mid)
