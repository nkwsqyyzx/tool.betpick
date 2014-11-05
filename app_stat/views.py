from django.shortcuts import render_to_response

# Create your views here.
from app_stat.tool import StatProvider


def stat_home(request):
    simple_soccer_stat = StatProvider.GetLeagues()
    return render_to_response('app_stat/templates/home.html', locals())


def stat_league(request):
    leagues = StatProvider.GetLeagues()
    return render_to_response('app_stat/templates/simple_soccer_stat/leagues.html', locals())


def stat_match(request, link, home, away):
    flag = 'espn=true' in link
    home = home.replace('_', ' ')
    away = away.replace('_', ' ')
    homeList, awayList = StatProvider.GetMatchesByLink(link)
    homeStatics = []
    for i in homeList:
        m = StatProvider.GetStatics(matchid=i, flag=flag)
        if m:
            homeStatics.append(m)
    awayStatics = []
    for i in awayList:
        m = StatProvider.GetStatics(matchid=i, flag=flag)
        if m:
            awayStatics.append(m)
    return render_to_response('app_stat/templates/simple_soccer_stat/against_stat.html', locals())


def stat_league_matches(request, leagueId, league):
    matches = StatProvider.GetMatchesLink(leagueId=leagueId)
    return render_to_response('app_stat/templates/simple_soccer_stat/leagues_matches.html', locals())


from app_stat.tool import WhoScoredDBProvider


def w_stat_league(request):
    return render_to_response('app_stat/templates/who_scored/leagues.html')


def w_stat_match(request, homeid, awayid, home, away):
    homeList = WhoScoredDBProvider.GetClubStatics(clubId=homeid)
    awayList = WhoScoredDBProvider.GetClubStatics(clubId=awayid)
    homeJS = ['var home = [];']
    for c in homeList:
        homeJS.append('mm = {};')
        homeJS.append('mm.data = ' + str(c) + ';')
        homeJS.append('home.push(mm);')
    homeJS = '\n'.join(homeJS)
    awayJS = ['var away = [];']
    for c in awayList:
        awayJS.append('mm = {};')
        awayJS.append('mm.data = ' + str(c) + ';')
        awayJS.append('away.push(mm);')
    awayJS = '\n'.join(awayJS)
    return render_to_response('app_stat/templates/who_scored/against_stat.html', locals())


def w_stat_league_matches(request, leagueURL, league):
    matches, id_match = WhoScoredDBProvider.GetMatchesLink(leagueURL=leagueURL)
    return render_to_response('app_stat/templates/who_scored/leagues_matches.html', locals())


def w_stat_club_matches(request, clubId):
    homeList = WhoScoredDBProvider.GetClubStatics(clubId=clubId)
    awayList = []
    homeJS = ['var home = [];']
    for a, b, c in homeList:
        homeJS.append('mm = {};')
        homeJS.append('mm.home = ' + a + ';')
        homeJS.append('mm.away = ' + b + ';')
        homeJS.append('mm.data = ' + c + ';')
        homeJS.append('home.push(mm);')
    homeJS = '\n'.join(homeJS)
    awayJS = ['var away = [];']
    for a, b, c in awayList:
        awayJS.append('mm = {};')
        awayJS.append('mm.home = ' + a + ';')
        awayJS.append('mm.away = ' + b + ';')
        awayJS.append('mm.data = ' + c + ';')
        awayJS.append('away.push(mm);')
    awayJS = '\n'.join(awayJS)
    return render_to_response('app_stat/templates/who_scored/against_stat.html', locals())


def w_stat_club_matches2(request, homeId, guestId):
    homeList = WhoScoredDBProvider.GetClubStatics(clubId=homeId)
    awayList = WhoScoredDBProvider.GetClubStatics(clubId=guestId)
    homeJS = ['var home = [];']
    for a, b, c in homeList:
        homeJS.append('mm = {};')
        homeJS.append('mm.home = ' + a + ';')
        homeJS.append('mm.away = ' + b + ';')
        homeJS.append('mm.data = ' + c + ';')
        homeJS.append('home.push(mm);')
    homeJS = '\n'.join(homeJS)
    awayJS = ['var away = [];']
    for a, b, c in awayList:
        awayJS.append('mm = {};')
        awayJS.append('mm.home = ' + a + ';')
        awayJS.append('mm.away = ' + b + ';')
        awayJS.append('mm.data = ' + c + ';')
        awayJS.append('away.push(mm);')
    awayJS = '\n'.join(awayJS)
    return render_to_response('app_stat/templates/who_scored/against_stat.html', locals())
