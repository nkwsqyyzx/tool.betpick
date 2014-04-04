# -*- coding: UTF8 -*-
from bs4 import BeautifulSoup
import re
import urllib

from app_odds.tool.MatchOdds import MatchOdds
from app_odds.tool.HtmlCache import HtmlCache

escape = urllib.parse.quote

cache = HtmlCache()
class OddsProvider():
    def __init__(self,mid):
        self.mid = mid
        self.url = 'http://api.zso8.com/a/y{0}cn.html'.format(mid)

    def __getAsianOddsHtml(self):
        return cache.getContent(self.url,timeout=1000000)

    def __parseHtmlToCompanyPairs(self,html):
        soup = BeautifulSoup(html)
        table = soup.find('table')
        rs = []
        trs = table.findAll('tr')[2:]
        r = re.compile(r'\(|,')
        for tr in trs:
            company = tr.find('div').get_text()
            # label 里面有访问结果所需的元素
            label = tr.find('label')
            onclick = label.get('onclick')
            m = ([i.replace("'",'') for i in r.split(onclick)])
            rs.append((company,m[2],m[3],m[4],m[5]))
        return rs

    def getResult(self,companyFilter = []):
        h = self.__getAsianOddsHtml()
        pairs = self.__parseHtmlToCompanyPairs(h)

        if companyFilter:
            a = [r for r in pairs if r[0] in companyFilter]
            for p in a:
                yield self.__getCompanyData(p)
        else:
            for p in pairs:
                yield self.__getCompanyData(p)

    def __parseTwoColumn(self, p, source, rs):
        soup = BeautifulSoup(source)
        trs = soup.findAll('tr')[2:]
        for tr in trs:
            tds = tr.findAll('td')
            t = tds[0].get_text().strip()
            if '市场倾向' in t:
                continue
            s1 = tds[1].get_text().strip()
            p = tds[2].get_text().strip()
            s2 = tds[3].get_text().strip()
            rs.append((t, s1, p, s2))

    def __getAsianOdds(self, p, ec, mid, cid, t1, t2, m):
        uri = 'http://app.zso8.com/midDetailA.aspx?a=1&id={0}&cid={1}&t1={2}&t2={3}&Company={4}'.format(mid, cid, t1, t2, ec)
        source = cache.getContent(uri)
        rs = m.asian
        self.__parseTwoColumn(p, source, rs)


    def __getOverOdds(self, p, ec, mid, cid, t1, t2, m):
        uri = 'http://app.zso8.com/midDetailU.aspx?id={0}&cid={1}&t1={2}&t2={3}&Company={4}'.format(mid, cid, t1, t2, ec)
        source = cache.getContent(uri)
        self.__parseTwoColumn(p, source, m.over)


    def __getEuroOdds(self, ec, mid, cid, t1, t2, m):
        uri = 'http://app.zso8.com/midDetailE.aspx?id={0}&cid={1}&t1={2}&t2={3}&Company={4}'.format(mid, cid, t1, t2, ec)
        source = cache.getContent(uri)
        soup = BeautifulSoup(source)
        trs = soup.find('table').findAll('tr')[2:-3]
        for tr in trs:
            tds = tr.findAll('td')
            # 变化时间
            time = tds[0].get_text().strip()
            # 主队赔率
            home = tds[1].get_text().strip()
            # 平局赔率
            draw = tds[2].get_text().strip()
            # 客队赔率
            away = tds[3].get_text().strip()
            # 返还率
            roi = tds[7].get_text().strip()
            i = time, home, draw, away, roi
            m.euro.append(i)

    def __getCompanyData(self,p):
        company = p[0]
        ec = escape(company)
        mid = p[1]
        cid = p[2]
        t1 = escape(p[3])
        t2 = escape(p[4])

        m = MatchOdds()
        m.home = p[3]
        m.away = p[4]

        self.__getAsianOdds(p, ec, mid, cid, t1, t2, m)
        # self.__getOverOdds(p, ec, mid, cid, t1, t2, m)
        self.__getEuroOdds(ec, mid, cid, t1, t2, m)

        m.company = company
        return m

if __name__ == "__main__":
    o = OddsProvider('681785')
    companyFilter = ['']
    rs = o.getResult()

    for r in rs:
        print(r.company)
        for a in r.asian:
            print(a)

        for a in r.euro:
            print(a)
