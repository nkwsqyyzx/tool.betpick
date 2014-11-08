import glob
import time
import pymysql

def createTable(cursor):
    cursor.execute('create table if not exists t_team(id INTEGER PRIMARY KEY, name varchar(64));')
    cursor.execute('create table if not exists t_match(id INTEGER PRIMARY KEY, statistics TEXT);')

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

def parseAllTeam(a):
    d = set()
    for i in a:
        i = i[1][0][0]
        d.add((i[0],i[2]))
        d.add((i[1],i[3]))
    return d

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


conn = pymysql.connect(host='localhost', user='yourusername', password='yourpassword', database='yourdatabase')
files = glob.glob('path/to/cache/htmls/*.html')


def dojob(conn, files):
    cursor = conn.cursor()
    createTable(cursor)
    all_matchs = src(files)
    id_teams = parseAllTeam(all_matchs)
    for i in id_teams:
        try:
            cursor.execute('insert into t_team values({0}, "{1}")'.format(i[0], i[1]))
            cursor.execute('create table if not exists t_team_match_{0}(id INTEGER PRIMARY KEY, time INTEGER);'.format(i[0]))
        except Exception as e:
            print(i, e)
    for i in a:
        r = i[1][0][0]
        (mid, t, home_id, guest_id) = (i[0], r[4], r[0], r[1])
        t = time.strptime(t, '%m/%d/%Y %H:%M:%S')
        t = time.mktime(time.localtime(time.mktime(t) + 8 * 60 * 60))
        t = int(t)
        try:
            cursor.execute('insert into t_team_match_{0} values({1}, {2})'.format(home_id, mid, t))
            cursor.execute('insert into t_team_match_{0} values({1}, {2})'.format(guest_id, mid, t))
        except Exception as e:
            print(r, e)
    for i in a:
        r = i[1][0][0]
        r = tr(str(i[1]).replace('None', ''))
        sql = 'insert into t_match values({0}, "{1}")'.format(i[0], r)
        try:
            cursor.execute(sql)
        except Exception as e:
            print(i[0], e, r)
            break;

for i in a:
    r = i[1][0][0]
    r = tr(str(i[1]).replace('None', ''))
    sql = 'insert into t_match values({0}, "{1}")'.format(i[0], r)
    try:
        cursor.execute(sql)
    except Exception as e:
        print(i[0], e, r)
        break;


for i in a:
    r = i[1][0][0]
    (mid, t, home_id, guest_id) = (i[0], r[4], r[0], r[1])
    t = time.strptime(t, '%m/%d/%Y %H:%M:%S')
    t = time.mktime(time.localtime(time.mktime(t) + 8 * 60 * 60))
    t = int(t)
    try:
        cursor.execute('insert into t_team_match_{0} values({1}, {2})'.format(home_id, mid, t))
        cursor.execute('insert into t_team_match_{0} values({1}, {2})'.format(guest_id, mid, t))
    except Exception as e:
        print(r, e)
