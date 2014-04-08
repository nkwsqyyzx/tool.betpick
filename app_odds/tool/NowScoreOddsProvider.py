# -*- coding: UTF8 -*-
from bs4 import BeautifulSoup

from app_odds.tool.MatchOdds import MatchOdds,Odds
from app_odds.tool.HtmlCache import HtmlCache

cache = HtmlCache()
allCompanies = [
        (1,"澳门"),
        (12,"易胜博"),
        (8,"Bet365"),
        (22,"10Bet"),
        (3,"SB"),
        (4,"立博"),
        (14,"韦德"),
        (17,"明陞"),
        (23,"金宝博"),
        (24,"沙巴"),
        (31,"利记"),
        (9,"威廉希尔"),
        (7,"SNAI"),
        (18,"EuroBet"),
        (19,"Inter wetten"),
        (35,"盈禾")
]

class NowScoreOddsProvider():
    def __init__(self,mid):
        self.mid = mid

    def __getOddsByCompanyId(self,cid):
        url = 'http://live1.nowscore.com/odds/3in1Odds.aspx?companyid={1}&id={0}'.format(self.mid,cid)
        return cache.getContent(url)

    def getResult(self,companyFilter = []):
        caredCompanies = None
        if companyFilter:
            caredCompanies = [a for a in allCompanies if a[1] in companyFilter]
        else:
            caredCompanies = [a for a in allCompanies[0:10]]
        matchOdds = MatchOdds()
        for c in caredCompanies:
            html = self.__getOddsByCompanyId(c[0])
            soup = BeautifulSoup(html)
            tables = soup.findAll('table',{"class":'gts',"bgcolor":"#DDDDDD"})
            o = Odds()
            o.company = c[1]
            # 亚盘
            for tr in tables[0].findAll('tr')[1:]:
                tds = tr.findAll('td')
                if len(tds) < 7 or tds[6].get_text().strip() == '滚':
                    continue
                t = tds[5].get_text().strip()
                t = '{0} {1}'.format(t[0:5],t[5:])
                s1 = tds[2].get_text().strip()
                p = tds[3].get_text().strip()
                s2 = tds[4].get_text().strip()
                o.asian.append((t,s1,p,s2))

            # 大小盘
            for tr in tables[1].findAll('tr')[1:]:
                tds = tr.findAll('td')
                if len(tds) < 7 or tds[6].get_text().strip() == '滚':
                    continue
                t = tds[5].get_text().strip()
                t = '{0} {1}'.format(t[0:5],t[5:])
                s1 = tds[2].get_text().strip()
                p = tds[3].get_text().strip()
                s2 = tds[4].get_text().strip()
                o.over.append((t,s1,p,s2))

            # 欧赔
            for tr in tables[2].findAll('tr')[1:]:
                tds = tr.findAll('td')
                if len(tds) < 7 or tds[6].get_text().strip() == '滚':
                    continue
                t = tds[5].get_text().strip()
                # 变化时间
                t = '{0} {1}'.format(t[0:5],t[5:])
                # 主队赔率
                s1 = tds[2].get_text().strip()
                # 平局赔率
                s2 = tds[3].get_text().strip()
                # 客队赔率
                s3 = tds[4].get_text().strip()
                # 返还率
                p = ('%.2f' % (100.0 * float(s1)*float(s2)*float(s3)/(float(s2)*float(s3)+float(s1)*float(s3)+float(s1)*float(s2))))
                o.euro.append((t,s1,s2,s3,p))
            matchOdds.odds.append(o)
        return matchOdds;

if __name__ == "__main__":
    o = NowScoreOddsProvider('853476')
    rs = o.getResult()

    for r in rs.odds:
        print(r.company)
        for a in r.asian:
            print(a)

        for a in r.euro:
            print(a)
