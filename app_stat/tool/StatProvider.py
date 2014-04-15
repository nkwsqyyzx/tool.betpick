# -*- coding: UTF8 -*-
# from app_odds.tool.MatchOdds import MatchOdds,Odds
# from app_odds.tool.HtmlCache import HtmlCache

from HtmlCache import HtmlCache

cache = HtmlCache(basepath='data/')
timeout = 7*24*60*60

class StatProvider():
    def __getHtml(self,matchid):
        url = 'http://www.simplesoccerstats.com/consoles/metrics/match.php?id={0}&espn=true'.format(matchid)
        return cache.getContent(url,timeout=timeout)

    def getResult(self,matchid):
        html = self.__getHtml(matchid)
        p = html.split('</br>')[1:]
        print('\n'.join(p))

from bs4 import BeautifulSoup
class B():
    def __getHtml(self,leagueId):
        url = 'http://www.simplesoccerstats.com/consoles/index.php?lge={0}'.format(leagueId)
        return cache.getContent(url,timeout=timeout)

    def getResult(self,leagueId):
        matches = []
        html = self.__getHtml(leagueId)
        soup = BeautifulSoup(html)
        sel_Match = soup.find('select',{'id':'sel_Match'})
        if sel_Match:
            for o in sel_Match.findAll('option'):
                value = o['value']
                if value:
                    v = value.split(':')
                    m = (v[1],v[2],v[3],v[4],v[5],v[6])
                    matches.append(m)
        return matches

if __name__ == "__main__":
    if 0:
        o = StatProvider()
        rs = o.getResult(matchid='367462')
    else:
        o = B()
        matches = o.getResult(0)
        for m in matches:
            print(m)
