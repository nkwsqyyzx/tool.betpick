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
        asianSource = self.__getAsianOddsHtml()
        pairs = self.__parseHtmlToCompanyPairs(asianSource)

        if companyFilter:
            selectedPairs = [pair for pair in pairs if pair[0] in companyFilter]
            for pair in selectedPairs:
                yield self.__getCompanyData(pair)
        else:
            for pair in pairs:
                yield self.__getCompanyData(pair)

    def __parseTwoColumn(self, source, rs):
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

    def __getAsianOdds(self, ec, mid, cid, t1, t2, m):
        uri = 'http://app.zso8.com/midDetailA.aspx?a=1&id={0}&cid={1}&t1={2}&t2={3}&Company={4}'.format(mid, cid, t1, t2, ec)
        source = cache.getContent(uri)
        rs = m.asian
        self.__parseTwoColumn(source, rs)

    def __getOverOdds(self, ec, mid, cid, t1, t2, m):
        uri = 'http://app.zso8.com/midDetailU.aspx?id={0}&cid={1}&t1={2}&t2={3}&Company={4}'.format(mid, cid, t1, t2, ec)
        source = cache.getContent(uri)
        self.__parseTwoColumn(source, m.over)

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

    def __getCompanyData(self,pair):
        company = pair[0]
        ec = escape(company)
        mid = pair[1]
        cid = pair[2]
        t1 = escape(pair[3])
        t2 = escape(pair[4])

        m = MatchOdds()
        m.home = pair[3]
        m.away = pair[4]

        self.__getAsianOdds(ec, mid, cid, t1, t2, m)
        # self.__getOverOdds(ec, mid, cid, t1, t2, m)
        self.__getEuroOdds(ec, mid, cid, t1, t2, m)

        m.company = company
        return m

class EuroOddsPairParser:
    def __init__(self,source):
        self.source = source

    def getResult(self):
        pairs = []
        return pairs

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
