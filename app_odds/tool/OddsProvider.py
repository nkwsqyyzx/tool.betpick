# -*- coding: UTF8 -*-
from bs4 import BeautifulSoup
import codecs
import os.path
import random
import re
import time
import urllib.request

from app_odds.tool.MatchOdds import MatchOdds

escape = urllib.parse.quote

cache = 1
release = 1
delay = 1

class OddsProvider():
    def __init__(self,mid):
        self.mid = mid
        self.url = 'http://api.zso8.com/a/y{0}cn.html'.format(mid)

    def __getAsianOddsHtml(self):
        return self.__getHtml(self.url)

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

    def __getHtml(self,u):
        if cache:
            import hashlib
            m = hashlib.md5()
            m.update(u.encode())
            md5value=m.hexdigest()

            fpath = './data/{0}.html'.format(md5value)
            if os.path.exists(fpath) and time.time() - os.path.getmtime(fpath) < (30 * 60):
                with codecs.open(fpath,'r','utf-8') as f:
                    return f.read()
            else:
                html = urllib.request.urlopen(u).read().decode('UTF-8')
                if not os.path.exists('./data/'):
                    os.makedirs('./data/')
                with codecs.open(fpath, 'w', 'utf-8') as outfile:
                    outfile.write(html)
                return html
        else:
            html = urllib.request.urlopen(u).read().decode('UTF-8')
            return html


    def __parseTwoColumn(self, p, source, rs):
        soup = BeautifulSoup(source)
        trs = soup.findAll('tr')[3:]
        for tr in trs:
            tds = tr.findAll('td')
            t = tds[0].get_text().strip()
            s1 = tds[1].get_text().strip()
            p = tds[2].get_text().strip()
            s2 = tds[3].get_text().strip()
            rs.append((t, s1, p, s2))

    def __getAsianOdds(self, p, ec, mid, cid, t1, t2, m):
        uri = 'http://app.zso8.com/midDetailA.aspx?a=1&id={0}&cid={1}&t1={2}&t2={3}&Company={4}'.format(mid, cid, t1, t2, ec)
        if release:
            source = self.__getHtml(uri)
        else:
            source = """
        <html><head><meta http-equiv=Content-Type content=text/html; charset=utf-8><title>查尔顿 VS 牛津联队 - 澳门让球盘走势</title><style>tr,td{font-family: 'Tahoma', '宋体';font-size: 12px;}.font12 {font-family: 'Tahoma', '宋体';font-size: 12px;}.font13 {font-family: 'Tahoma', '宋体';font-size: 13px;}</style></head><body leftmargin='1' topmargin='1' bgcolor=#ffffff><table width=390  border=0 align=center cellpadding=1 cellspacing=1 bgcolor=#bbbbbb><tbody><tr><td colspan='4' align='center' style='background-color:#cc3300;color:white;font-size:14px;'>查尔顿VS牛津联队--澳门 - 让球盘走势</td></tr><tr align=center bgcolor=#ffffaa class=font13 height=24><td width='123' align='center'><b><FONT color=#00000>变化时间</font></b></td><td><b><FONT color=#000000>主队</font></b></td><td><b><FONT color=#000000>盘口</font></b></td><td><b><FONT color=#000000>客队</font></b></td></tr><tr align=center bgcolor=#ffffcc class=font13 height=24><td width='123'><FONT color=#00000>&nbsp;&nbsp;市场倾向→</font></td><td><FONT color=#000000 title='主队投注比例'>160000</font></td><td><FONT color=#000000 title='两队投注比例百分比(仅供参考)'>28.07%/71.93%</font></td><td><FONT color=#000000 title='客队投注比例'>410000</font></td></tr><tr align=center bgcolor=#f1f7f1><td height=22 class=font12 align=left>&nbsp;&nbsp;01-15 03:08:49</td><td><font color='red'><b>1.05</b></font></td><td>半球/一球</td><td> <font color='green'><b>0.75</b></font></td></tr><tr align=center bgcolor=#ffffff><td height=22 class=font12 align=left>&nbsp;&nbsp;01-15 03:08:09</td><td><font color='red'><b>1.00</b></font></td><td>半球/一球</td><td> <font color='green'><b>0.80</b></font></td></tr><tr align=center bgcolor=#f1f7f1><td height=22 class=font12 align=left>&nbsp;&nbsp;01-15 01:57:02</td><td><font color='red'><b>0.88</b></font></td><td>半球/一球</td><td> <font color='green'><b>0.92</b></font></td></tr><tr align=center bgcolor=#ffffff><td height=22 class=font12 align=left>&nbsp;&nbsp;01-14 21:41:32</td><td><font color='green'><b>0.80</b></font></td><td>半球/一球</td><td> <font color='red'><b>1.00</b></font></td></tr><tr align=center bgcolor=#f1f7f1><td height=22 class=font12 align=left>&nbsp;&nbsp;01-14 11:04:32</td><td><font color='green'><b>0.82</b></font></td><td>半球/一球</td><td> <font color='red'><b>0.98</b></font></td></tr><tr align=center bgcolor=#ffffff><td height=22 class=font12 align=left>&nbsp;&nbsp;01-06 17:42:54</td><td><font color='green'><b>0.96</b></font></td><td>半球/一球</td><td> <font color='red'><b>0.84</b></font></td></tr><tr align=center bgcolor=#f1f7f1><td height=22 class=font12 align=left>&nbsp;&nbsp;01-02 16:25:08</td><td><font color='red'><b>1.08</b></font></td><td>一球</td><td> <font color='green'><b>0.72</b></font></td></tr><tr align=center bgcolor=#ffffff><td height=22 class=font12 align=left>&nbsp;&nbsp;01-01 21:19:50</td><td><font color='red'><b>1.00</b></font></td><td>一球</td><td> <font color='green'><b>0.80</b></font></td></tr><tr align=center bgcolor=#f1f7f1><td height=22 class=font12 align=left>&nbsp;&nbsp;12-31 18:49:13</td><td><font color='black'><b>0.92</b></font></td><td>一球</td><td> <font color='black'><b>0.88</b></font></td></tr></tbody></table></body></html>
        """
        rs = m.asian
        self.__parseTwoColumn(p, source, rs)


    def __getOverOdds(self, p, ec, mid, cid, t1, t2, m):
        uri = 'http://app.zso8.com/midDetailU.aspx?id={0}&cid={1}&t1={2}&t2={3}&Company={4}'.format(mid, cid, t1, t2, ec)
        if release:
            source = self.__getHtml(uri)
        else:
            source = """
        <html><head><meta http-equiv=Content-Type content=text/html; charset=utf-8><title>查尔顿 VS 牛津联队 - 澳门大小盘走势</title><style>tr,td{font-family: 'Tahoma', '宋体';font-size: 12px;}.font12 {font-family: 'Tahoma', '宋体';font-size: 12px;}.font13 {font-family: 'Tahoma', '宋体';font-size: 13px;}</style></head><body  leftmargin='1' topmargin='1' bgcolor=#ffffff><table width=390  border=0 align=center cellpadding=1 cellspacing=1 bgcolor=#bbbbbb><tbody><tr><td colspan='4' align='center' style='background-color:#cc3300;color:white;font-size:14px;'>查尔顿VS牛津联队--澳门 - 大小盘走势</td></tr><tr align=center bgcolor=#ffffaa class=font13 height=24><td width='120' align='center'><b><FONT color=#00000>变化时间</font></b></td><td><b><FONT color=#000000>大球</font></b></td><td><b><FONT color=#000000>盘口</font></b></td><td><b><FONT color=#000000>小球</font></b></td></tr><tr align=center bgcolor=#ffffcc class=font13 height=24><td width='120'><FONT color=#00000>&nbsp;&nbsp;市场倾向→</font></td><td><FONT color=#000000 title='主队投注比例'>170000</font></td><td><FONT color=#000000 title='两队投注比例百分比(仅供参考)'>43.59%/56.41%</font></td><td><FONT color=#000000 title='客队投注比例'>220000</font></td></tr><tr align=center bgcolor=#ffffff><td height=22 class=font12 align=left>&nbsp;&nbsp;01-15 03:44:48</td><td><font color='red'><b>1.00</b></font></td><td>2.5 球</td><td> <font color='green'><b>0.70</b></font></td></tr><tr align=center bgcolor=#f1f7f1><td height=22 class=font12 align=left>&nbsp;&nbsp;01-14 21:35:51</td><td><font color='green'><b>0.88</b></font></td><td>2.5 球</td><td> <font color='red'><b>0.82</b></font></td></tr><tr align=center bgcolor=#ffffff><td height=22 class=font12 align=left>&nbsp;&nbsp;01-14 11:27:25</td><td><font color='red'><b>0.90</b></font></td><td>2.5 球</td><td> <font color='green'><b>0.80</b></font></td></tr><tr align=center bgcolor=#f1f7f1><td height=22 class=font12 align=left>&nbsp;&nbsp;01-06 17:42:51</td><td><font color='green'><b>0.85</b></font></td><td>2.5 球</td><td> <font color='red'><b>0.85</b></font></td></tr><tr align=center bgcolor=#ffffff><td height=22 class=font12 align=left>&nbsp;&nbsp;01-03 17:02:52</td><td><font color='red'><b>1.00</b></font></td><td>2.5/3 球</td><td> <font color='green'><b>0.70</b></font></td></tr><tr align=center bgcolor=#f1f7f1><td height=22 class=font12 align=left>&nbsp;&nbsp;12-31 18:49:13</td><td><font color='black'><b>0.95</b></font></td><td>2.5/3 球</td><td> <font color='black'><b>0.75</b></font></td></tr></tbody></table></body></html>
        """
        soup = BeautifulSoup(source)
        self.__parseTwoColumn(p, source, m.over)


    def __getEuroOdds(self, ec, mid, cid, t1, t2, m):
        uri = 'http://app.zso8.com/midDetailE.aspx?id={0}&cid={1}&t1={2}&t2={3}&Company={4}'.format(mid, cid, t1, t2, ec)
        if release:
            source = self.__getHtml(uri)
        else:
            source = """
        <html><head><title>标准盘历史走势</title><meta http-equiv='Content-Type' content='text/html; charset=utf-8'><meta http-equiv='pragma' content='no-cache'><meta http-equiv='Cache-Control' content='no-cache'><meta http-equiv='Cache-Control' content='no-cache, must-revalidate'><style type='text/css'>tr,td{font-family: 'Tahoma', '宋体';font-size:12px;text-align:center ;}.f12{font-size: 12px;}</style></head><body leftmargin='1' topmargin='1'><div id='odds'><table width=468  border=0 align=center cellpadding=1 cellspacing=1 bgcolor=#bbbbbb><tr><td colspan=8 style='background-color:#cc3300;color:white;font-size:14px;'>查尔顿 VS 牛津联队 --Crown &nbsp; 标准盘走势</td></tr><tr bgcolor=#ffffaa align=center style='font-weight:bold'><td width=120>变化时间</td><td width=40>主嬴</td><td width=40>和</td><td width=40>客嬴</td><td>主胜率</td><td>和率</td><td>客胜率</td><td>返还率</td></tr><tr height=22 bgcolor=#ffffff><td>01-15 03:30:21</td><td  style='color:green'>1.75</td><td >3.40</td><td  style='color:red'>4.60</td><td>52.77%</td><td>27.16%</td><td>20.07%</td><td>92.34%</td></tr><tr height=22 bgcolor=#f1f7f1><td>01-15 02:57:35</td><td  style='color:red'>1.76</td><td >3.40</td><td  style='color:green'>4.55</td><td>52.51%</td><td>27.18%</td><td>20.31%</td><td>92.41%</td></tr><tr height=22 bgcolor=#ffffff><td>01-15 02:49:50</td><td  style='color:red'>1.75</td><td >3.40</td><td  style='color:green'>4.60</td><td>52.77%</td><td>27.16%</td><td>20.07%</td><td>92.34%</td></tr><tr height=22 bgcolor=#f1f7f1><td>01-15 02:23:12</td><td  style='color:green'>1.73</td><td >3.40</td><td >4.70</td><td>53.28%</td><td>27.11%</td><td>19.61%</td><td>92.17%</td></tr><tr height=22 bgcolor=#ffffff><td>01-15 01:58:01</td><td  style='color:red'>1.74</td><td >3.40</td><td  style='color:green'>4.70</td><td>53.14%</td><td>27.19%</td><td>19.67%</td><td>92.46%</td></tr><tr height=22 bgcolor=#f1f7f1><td>01-15 01:56:09</td><td  style='color:green'>1.73</td><td >3.40</td><td  style='color:red'>4.75</td><td>53.39%</td><td>27.17%</td><td>19.44%</td><td>92.36%</td></tr><tr height=22 bgcolor=#ffffff><td>01-15 01:55:51</td><td  style='color:red'>1.74</td><td >3.40</td><td >4.65</td><td>53.02%</td><td>27.14%</td><td>19.84%</td><td>92.26%</td></tr><tr height=22 bgcolor=#f1f7f1><td>01-15 01:55:14</td><td  style='color:green'>1.71</td><td >3.40</td><td >4.65</td><td>53.46%</td><td>26.89%</td><td>19.66%</td><td>91.41%</td></tr><tr height=22 bgcolor=#ffffff><td>01-15 01:54:41</td><td  style='color:red'>1.74</td><td  style='color:green'>3.40</td><td  style='color:green'>4.65</td><td>53.02%</td><td>27.14%</td><td>19.84%</td><td>92.26%</td></tr><tr height=22 bgcolor=#f1f7f1><td>01-15 01:29:28</td><td  style='color:red'>1.67</td><td  style='color:green'>3.70</td><td  style='color:green'>4.70</td><td>55.35%</td><td>24.98%</td><td>19.67%</td><td>92.44%</td></tr><tr height=22 bgcolor=#ffffff><td>01-15 01:28:50</td><td  style='color:red'>1.65</td><td >3.75</td><td  style='color:green'>4.80</td><td>56.06%</td><td>24.67%</td><td>19.27%</td><td>92.50%</td></tr><tr height=22 bgcolor=#f1f7f1><td>01-15 01:27:27</td><td >1.63</td><td >3.75</td><td  style='color:green'>4.95</td><td>56.69%</td><td>24.64%</td><td>18.67%</td><td>92.41%</td></tr><tr height=22 bgcolor=#ffffff><td>01-15 01:27:15</td><td  style='color:red'>1.63</td><td >3.75</td><td >5.00</td><td>56.80%</td><td>24.69%</td><td>18.52%</td><td>92.58%</td></tr><tr height=22 bgcolor=#f1f7f1><td>01-15 01:25:02</td><td  style='color:red'>1.62</td><td >3.75</td><td  style='color:green'>5.00</td><td>56.95%</td><td>24.60%</td><td>18.45%</td><td>92.26%</td></tr><tr height=22 bgcolor=#ffffff><td>01-15 00:14:12</td><td  style='color:green'>1.60</td><td  style='color:red'>3.75</td><td  style='color:red'>5.30</td><td>57.85%</td><td>24.68%</td><td>17.46%</td><td>92.56%</td></tr><tr height=22 bgcolor=#f1f7f1><td>01-15 00:11:39</td><td >1.62</td><td >3.70</td><td  style='color:red'>5.10</td><td>56.96%</td><td>24.94%</td><td>18.09%</td><td>92.28%</td></tr><tr height=22 bgcolor=#ffffff><td>01-15 00:11:24</td><td  style='color:green'>1.62</td><td >3.70</td><td >5.00</td><td>56.76%</td><td>24.85%</td><td>18.39%</td><td>91.95%</td></tr><tr height=22 bgcolor=#f1f7f1><td>01-14 21:00:19</td><td  style='color:green'>1.63</td><td  style='color:red'>3.70</td><td >5.00</td><td>56.61%</td><td>24.94%</td><td>18.45%</td><td>92.27%</td></tr><tr height=22 bgcolor=#ffffff><td>01-14 14:32:24</td><td >1.65</td><td >3.60</td><td  style='color:red'>5.00</td><td>55.92%</td><td>25.63%</td><td>18.45%</td><td>92.26%</td></tr><tr height=22 bgcolor=#f1f7f1><td>01-14 14:30:05</td><td  style='color:green'>1.65</td><td >3.60</td><td >4.85</td><td>55.60%</td><td>25.48%</td><td>18.92%</td><td>91.74%</td></tr><tr height=22 bgcolor=#ffffff><td>01-14 11:16:30</td><td  style='color:red'>1.67</td><td >3.60</td><td  style='color:red'>4.85</td><td>55.30%</td><td>25.65%</td><td>19.04%</td><td>92.36%</td></tr><tr height=22 bgcolor=#f1f7f1><td>01-10 19:11:37</td><td  style='color:green'>1.65</td><td  style='color:red'>3.60</td><td  style='color:red'>4.60</td><td>55.03%</td><td>25.22%</td><td>19.74%</td><td>90.81%</td></tr><tr height=22 bgcolor=#ffffff><td>01-06 21:36:22</td><td  style='color:red'>1.75</td><td  style='color:green'>3.50</td><td  style='color:green'>4.10</td><td>51.90%</td><td>25.95%</td><td>22.15%</td><td>90.82%</td></tr><tr height=22 bgcolor=#f1f7f1><td>01-06 00:50:53</td><td  style='color:red'>1.58</td><td  style='color:green'>3.70</td><td  style='color:green'>5.00</td><td>57.37%</td><td>24.50%</td><td>18.13%</td><td>90.65%</td></tr><tr height=22 bgcolor=#ffffff><td>01-05 16:44:08</td><td  style='color:green'>1.55</td><td  style='color:red'>3.80</td><td  style='color:red'>5.20</td><td>58.62%</td><td>23.91%</td><td>17.47%</td><td>90.86%</td></tr><tr height=22 bgcolor=#f1f7f1><td>01-03 15:30:02</td><td  style='color:red'>1.70</td><td  style='color:green'>3.55</td><td  style='color:green'>4.30</td><td>53.36%</td><td>25.55%</td><td>21.09%</td><td>90.70%</td></tr><tr height=22 bgcolor=#ffffff><td>01-02 16:37:57</td><td  style='color:red'>1.58</td><td >3.80</td><td  style='color:green'>4.90</td><td>57.53%</td><td>23.92%</td><td>18.55%</td><td>90.90%</td></tr><tr height=22 bgcolor=#f1f7f1><td>12-30 17:28:35</td><td  style='color:red'>1.55</td><td >3.80</td><td  style='color:green'>5.20</td><td>58.62%</td><td>23.91%</td><td>17.47%</td><td>90.86%</td></tr><tr height=22 bgcolor=#ffffff><td>12-30 17:12:53</td><td >1.50</td><td >3.80</td><td >5.90</td><td>60.64%</td><td>23.94%</td><td>15.42%</td><td>90.97%</td></tr><tr bgcolor=#ffdddd height=20><td>最大值</td><td>1.76</td><td>3.80</td><td>5.90</td><td>60.64%</td><td>27.19%</td><td>22.15%</td><td>92.58%</td></tr><tr bgcolor=#ecffec height=20><td>最小值</td><td>1.50</td><td>3.40</td><td>4.10</td><td>51.90%</td><td>23.91%</td><td>15.42%</td><td>90.65%</td></tr><tr bgcolor=#cae4ff height=20><td>平均值</td><td>1.66</td><td>3.60</td><td>4.85</td><td>55.42%</td><td>25.54%</td><td>19.03%</td><td>91.87%</td></tr></table></div></body></html>
        """
        soup = BeautifulSoup(source)
        trs = soup.find('table').findAll('tr')[2:-3]
        for tr in trs:
            tds = tr.findAll('td')
            time = tds[0].get_text().strip()
            home = tds[1].get_text().strip()
            draw = tds[2].get_text().strip()
            away = tds[3].get_text().strip()
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
        self.__getOverOdds(p, ec, mid, cid, t1, t2, m)
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
