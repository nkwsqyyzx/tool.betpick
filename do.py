import sqlite3
import time
import glob

def src(files):
    result = []
    for a in files:
        with  open(a) as f:
            try:
                lines = f.readlines()
                parseDataFromHtml(lines, result)
            except Exception as e:
                print(a, e)
    return result

def parseDataFromHtml(lines, result):
    match_id = 0
    data = []
    '''
    解析比赛id
    '''
    for line in lines:
        if 'var gLoginUrl =' in line:
            line = line.split('/Matches/')[1]
            line = line.split('/MatchReport')[0]
            match_id = int(line)
            break
    '''
    解析统计数据
    '''
    html = ''.join(lines)
    if 'var matchStats = ' in html:
        d = html.split('var matchStats = ')[1]
        d = d.split('var liveTeamStatsInfoConfig =')[0].replace('\n', '').replace(';', '').strip()
        while ',,' in d:
            d = d.replace(',,' , ',None,')
        data = eval(d)
    if match_id > 0 and len(data) > 0:
        result.append((match_id, data))

def h(a):
    d = []
    for i in a:
        i = i[1][0][0]
        d.append((i[0],i[2]))
        d.append((i[1],i[3]))
    return set(d)

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
        s2 = s2.replace('"', "'").replace("'", '-')
        s3 = r[i2+1:]
        r = s1 + s2 + s3
        i1 = i2 + 2
    return r

def dojob():
    conn = sqlite3.connect('db')
    cursor = conn.cursor()
    cursor.execute('create table if not exists t_team(id INTEGER PRIMARY KEY, name TEXT)')
    cursor.execute('create table if not exists t_team_match(mid INTEGER PRIMARY KEY, time INTEGER, home_id INTEGER, guest_id INTEGER)')
    cursor.execute('create table if not exists t_match(id INTEGER PRIMARY KEY, statistics TEXT)')
    files = glob.glob('/Users/wsq/tool.betpick/bin/whoscored/*.html')
    a = src(files)
    d = h(a)
    for i in d:
        try:
            cursor.execute('insert into t_team values({0}, "{1}")'.format(i[0], i[1]))
        except Exception as e:
            print(i, e)
    for i in a:
        r = i[1][0][0]
        (mid, t, home_id, guest_id) = (i[0], r[4], r[0], r[1])
        t = time.strptime(t, '%m/%d/%Y %H:%M:%S')
        t = time.mktime(time.localtime(time.mktime(t) + 8 * 60 * 60))
        t = int(t)
        try:
            cursor.execute('insert into t_team_match values({0}, {1}, {2}, {3})'.format(mid, t, home_id, guest_id))
        except Exception as e:
            print(r, e)
    # 需要解决双引号插入数据库的问题
    for i in a:
        r = i[1][0][0]
        r = tr(str(i[1]).replace('None', ''))
        sql = 'insert into t_match values({0}, "{1}")'.format(i[0], r)
        cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

