# -*- coding: UTF8 -*-
if __name__ == "__main__":
    from HtmlCache import HtmlCache
else:
    from app_stat.tool.HtmlCache import HtmlCache

cache = HtmlCache(basepath='bin/statics/')
timeout = 2*24*60*60

from bs4 import BeautifulSoup
def GetMatchesLink(leagueId):
    # 从每个联赛中获取下一轮比赛对阵链接
    url = 'http://www.simplesoccerstats.com/consoles/index.php?lge={0}'.format(leagueId)
    html = cache.getContent(url,timeout=timeout)
    soup = BeautifulSoup(html)
    sel_Match = soup.find('select',{'id':'sel_Match'})
    if "var espn = 'true';" in html:
        espn = 'true'
    else:
        espn = 'false'
    matches = []
    if sel_Match:
        for o in sel_Match.findAll('option'):
            value = o['value']
            if value:
                v = value.split(':')
                m = (0,v[1],v[2],v[3],v[4],v[5],v[6])
                homeTeam = m[1].replace(' ', "_")
                awayTeam = m[2].replace(' ', "_")
                homeMC = m[3]
                awayMC = m[5]
                homeTC = m[4]
                awayTC = m[6]
                hora = 'both'
                uri = "http://www.simplesoccerstats.com/consoles/metrics/matches.php?home=" + homeTeam + "&away=" + awayTeam + "&HMC=" + homeMC + "&HTC=" + homeTC + "&AMC=" + awayMC + "&ATC=" + awayTC + "&hora=" + hora + "&espn=" + espn
                matches.append((homeTeam,awayTeam,uri))
    return matches

def GetLeagues():
    # 获取所有支持的联赛
    leagues = []
    url = 'http://www.simplesoccerstats.com/consoles/index.php?lge=0'
    html = cache.getContent(url,timeout=timeout)
    soup = BeautifulSoup(html)
    sel_League = soup.find('select',{'id':'sel_League'})
    if sel_League:
        for option in sel_League.findAll('option'):
            value = option['value']
            leagues.append((option.get_text().strip(),value))
    return leagues

def GetMatchesByLink(link):
    # 从对阵链接中获取对应比赛的统计链接
    html = cache.getContent(link,timeout=timeout)
    soup = BeautifulSoup(html)
    idshome = []
    tds = soup.find('div',{'class':'matchboxL'}).findAll('td',{'class':'matchid'})
    for td in tds:
        mid = td['id']
        if mid:
            idshome.append(mid)

    idsaway = []
    tds = soup.find('div',{'class':'matchboxR'}).findAll('td',{'class':'matchid'})
    for td in tds:
        mid = td['id']
        if mid:
            idsaway.append(mid)
    return (idshome,idsaway)

import time
def GetStatics(matchid,flag):
    # 获取比赛统计数据
    # (时间,对阵双方,比分,半场比分,射门,射正,角球,首先达到3角球,首先达到5角球,首先达到7角球,犯规,黄牌,红牌,越位,控球率)
    url = 'http://www.simplesoccerstats.com/consoles/metrics/match.php?id={0}&espn={1}'.format(matchid,('true' if flag else 'false'))
    # 数据缓存4个月
    html = cache.getContent(url,timeout=4*30*24*60*60)
    p = html.split('</br>')[1:-1]
    t = time.strftime('%Y-%m-%d',time.strptime(p[0],'%d %b %y'))
    p1 = p[1].replace('<strong>','').replace('</strong>','').split(' v ')
    p2 = p[2].split(' FT ')
    p3 = p[3].split(' HT ')
    p4 = p[4].split(' Shots ')
    p5 = p[5].split(' Shots on Target ')
    p6 = p[6].split(' Corners ')
    if ' Race to 3 ' in html:
        p7 = p[7].split(' Race to 3 ')
        p8 = p[8].split(' Race to 5 ')
        p9 = p[9].split(' Race to 7 ')
        p10 = p[10].split(' Fouls ')
        p11 = p[11].split(' Yellow Cards ')
        p12 = p[12].split(' Red Cards ')
        p13 = p[13].split(' Offsides ')
        p14 = p[14].split(' Possession ')
    else:
        p7 = ['-','-']
        p8 = ['-','-']
        p9 = ['-','-']
        p10 = p[7].split(' Fouls ')
        p11 = p[8].split(' Yellow Cards ')
        p12 = p[9].split(' Red Cards ')
        p13 = ['-','-']
        p14 = ['-','-']


    home = Stat()
    home.team = p1[0]
    home.score = p2[0]
    home.halfScore = p3[0]
    home.shots = p4[0]
    home.shotsOn = p5[0]
    home.corners = p6[0]
    home.R3 = p7[0]
    home.R5 = p8[0]
    home.R7 = p9[0]
    home.foul = p10[0]
    home.yellow = p11[0]
    home.red = p12[0]
    home.offsides = p13[0]
    home.possession = p14[0]

    away = Stat()
    away.team = p1[1]
    away.score = p2[1]
    away.halfScore = p3[1]
    away.shots = p4[1]
    away.shotsOn = p5[1]
    away.corners = p6[1]
    away.R3 = p7[1]
    away.R5 = p8[1]
    away.R7 = p9[1]
    away.foul = p10[1]
    away.yellow = p11[1]
    away.red = p12[1]
    away.offsides = p13[1]
    away.possession = p14[1]

    return (t,home,away)

class Stat:
    def __init__(self):
        # 球队
        self.team = ''
        # 进球数
        self.score = ''
        # 半场进球数
        self.halfScore = ''
        # 射门
        self.shots = ''
        # 射正
        self.shotsOn = ''
        # 角球
        self.corners = ''
        # 首先达到3角球
        self.R3 = ''
        # 首先达到5角球
        self.R5 = ''
        # 首先达到7角球
        self.R7 = ''
        # 犯规
        self.foul = ''
        # 黄牌数
        self.yellow = ''
        # 红牌数
        self.red = ''
        # 越位数
        self.offsides = ''
        # 控球率
        self.possession = ''

    def __repr__(self):
        return str({"team":self.team , "score":self.score , "halfScore":self.halfScore , "shots":self.shots , "shotsOn":self.shotsOn , "corners":self.corners , "R3":self.R3 , "R5":self.R5 , "R7":self.R7 , "foul":self.foul , "yellow":self.yellow , "red":self.red , "offsides":self.offsides , "possession":self.possession})


if __name__ == "__main__":
    # home,away,link = GetMatchesLink(leagueId=0)[1]
    # homeMatches,awayMatches = GetMatchesByLink(link=link)
    # for matchid in homeMatches:
    #     t,h,a = GetStatics(matchid=matchid)
    #     print(t,h,a)
    #     break;
    t,h,a = GetStatics(matchid='862',flag=False)
