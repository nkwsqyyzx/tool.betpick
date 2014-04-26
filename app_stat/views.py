from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
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

def stat_league(request):
    leagues = StatProvider.GetLeagues()
    return render_to_response('app_stat/templates/app_stat/leagues.html',locals())

def stat_match(request,link,home,away):
    flag = 'espn=true' in link;
    home = home.replace('_',' ')
    away = away.replace('_',' ')
    homeList,awayList = StatProvider.GetMatchesByLink(link)
    homeStatics = []
    for i in homeList:
        homeStatics.append(StatProvider.GetStatics(matchid=i,flag=flag))
    awayStatics = []
    for i in awayList:
        awayStatics.append(StatProvider.GetStatics(matchid=i,flag=flag))
    return render_to_response('app_stat/templates/app_stat/against_stat.html',locals())

def stat_league_matches(request,leagueId,league):
    matches = StatProvider.GetMatchesLink(leagueId=leagueId)
    return render_to_response('app_stat/templates/app_stat/leagues_matches.html',locals())
