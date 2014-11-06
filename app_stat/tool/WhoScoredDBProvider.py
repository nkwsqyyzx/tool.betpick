# -*- coding: UTF8 -*-
if __name__ == "__main__":
    from HtmlCache import HtmlCache
else:
    from app_stat.tool.HtmlCache import HtmlCache

import sqlite3
import time

cache = HtmlCache(basepath='bin/whoscored/')
timeout = 2 * 24 * 60 * 60

def GetMatchesLink(leagueURL='Regions/252/Tournaments/7/England-Championship'):
    # 从每个联赛中获取下一轮比赛对阵链接
    url = 'http://www.whoscored.com/{0}'.format(leagueURL)
    html, cached = cache.getContentWithAgent(url=url, encoding='gbk',timeout=24*60*60)
    js = html.split('calendar.parameter()), ')[1].split(']);')[0].replace('\r\n', '')
    js = 'var matches = {0}];'.format(js)

    aa = 'var id_match = [[{0}];'.format(']')
    return js, aa

def GetMatchesByClub(clubId=15):
    # 从球队链接中获取其所有比赛号
    # => list of (matchid,home,away)
    link = 'http://www.whoscored.com/Teams/{0}/Fixtures/'.format(clubId)
    html, cached = cache.getContentWithAgent(url=link, encoding='gbk',timeout=3*24*60*60)
    # if cached:
    #        return
    # 保存对阵列表
    conn = sqlite3.connect('db')
    cursor = conn.cursor()
    try:
        hs = html.split('parametersCopy), ')
        js = hs[1].split('var teamFixtures ')[0].replace('\r\n', '')[0:-2]
        js = js.replace(',,',',None,')
        sql = 'insert or ignore into t_team values({0},"{1}")'
        allMatches = eval(js)
        for j in allMatches:
            # 根据who_scored网站的规则判断是否有赛后报告
            if j[1] == 1 and (j[26] == 1 or j[27] == 1) and (not matchHasTerminatedUnexpectedly(j[14])):
                pass
            else:
                continue
            m = j
            # 保存对阵信息
            match_id = m[0]
            home_id = m[4]
            home_name = m[5]
            guest_id = m[7]
            guest_name = m[8]
            t = m[2] + " " + m[3]
            t = time.strptime(t, '%d-%m-%Y %H:%M')
            t = int(time.mktime(time.localtime(time.mktime(t) + 8 * 60 * 60)))
            cursor.execute(sql.format(home_id, home_name))
            cursor.execute(sql.format(guest_id, guest_name))
            try:
                cursor.execute('insert or ignore into t_team_match_{0} values({1}, {2})'.format(home_id, match_id, t))
            except Exception as e:
                cursor.execute('create table if not exists t_team_match_{0}(id INTEGER PRIMARY KEY, time INTEGER)'.format(home_id))
                cursor.execute('insert or ignore into t_team_match_{0} values({1}, {2})'.format(home_id, match_id, t))
            try:
                cursor.execute('insert or ignore into t_team_match_{0} values({1}, {2})'.format(guest_id, match_id, t))
            except Exception as e:
                cursor.execute('create table if not exists t_team_match_{0}(id INTEGER PRIMARY KEY, time INTEGER)'.format(guest_id))
                cursor.execute('insert or ignore into t_team_match_{0} values({1}, {2})'.format(guest_id, match_id, t))
        conn.commit()
    except Exception as e:
        print("GetMatchesByClub", clubId, e)
        conn.rollback()
    cursor.close()
    conn.close()

def matchHasTerminatedUnexpectedly(status):
    return status == 'Abd' or status == "Post" or status == "Can" or status == "Susp"

def tr(s):
    i1 = 0
    i2 = 1
    r = s
    while True:
        i1 = r.find('"', i1)
        i2 = r.find('"', i1 + 1)
        if i1 < 0 or i2 < 0:
            break;
        s1 = r[0:i1]
        s2 = r[i1:i2+1]
        s2 = s2.replace("'", '-')
        s2 = s2.replace('"', "'")
        s3 = r[i2+1:]
        r = s1 + s2 + s3
        i1 = i2 + 2
    return r


def GetJSDataByMatchid(conn, matchid='758062'):
    cursor = conn.cursor()
    sql = 'select * from t_match where id={0}'
    cursor.execute(sql.format(matchid))
    d = None
    row = cursor.fetchone()
    if not row:
        try:
            url = 'http://www.whoscored.com/Matches/{0}/MatchReport'.format(matchid)
            html, cached = cache.getContentWithAgent(url=url, encoding='gbk',timeout=30*24*60*60)
            if 'var matchStats = ' in html:
                d = html.split('var matchStats = ')[1]
                d = d.split('var liveTeamStatsInfoConfig =')[0]
                d = d.replace('\r', '')
                d = d.replace('\n', '')
                d = d.replace(';', '')
                i = d.find(']')
                m = d[3:i].split(',')
                match_id = matchid
                home_id = m[0]
                home_name = m[2]
                guest_id = m[1]
                guest_name = m[3]
                t = m[4]
                t = time.strptime(t, "'%m/%d/%Y %H:%M:%S'")
                t = int(time.mktime(time.localtime(time.mktime(t) + 8 * 60 * 60)))
                sql = 'insert or ignore into t_team values({0},"{1}")'
                cursor.execute(sql.format(home_id, home_name))
                cursor.execute(sql.format(guest_id, guest_name))
                sql = 'insert or ignore into t_match values({0}, "{1}")'
                cursor.execute(sql.format(match_id, tr(d)))
        except Exception as e:
            print(url, d, e)
    else:
        d = row[1]

    cursor.close()
    return d

import time
def GetClubStatics(clubId):
    GetMatchesByClub(clubId)
    conn = sqlite3.connect('db')
    cursor = conn.cursor()
    sql = 'select t.id, tm.statistics from (select id from t_team_match_{0} order by time desc limit 15) t left join t_match tm on tm.id = t.id'
    cursor.execute(sql.format(clubId))
    d = []
    flag = False
    for row in cursor:
        if not row[1]:
            flag = True
            d.append(GetJSDataByMatchid(conn, row[0]))
        else:
            d.append(row[1])
    if flag:
        conn.commit()
    cursor.close()
    conn.close()
    return d

if __name__ == "__main__":
    GetJSDataByMatchid(720817)

