import glob
import time
files = glob.glob('/Users/wsq/tool.betpick/bin/whoscored/*.html')
import sqlite3
conn = sqlite3.connect('db')
cursor = conn.cursor()

def src():
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

a = src()
def h():
    d = []
    for i in a:
        i = i[1][0][0]
        d.append((i[0],i[2]))
        d.append((i[1],i[3]))
    return d

d = h()
for i in d:
    try:
        cursor.execute('insert into t_team values({0}, "{1}")'.format(i[0], i[1]))
    except Exception as e:
        print(i, e)

for i in a:
    r = i[1][0][0]
    (mid, home_id, guest_id) = (i[0], r[0], r[1])
    try:
        cursor.execute('insert into t_team_match values({0}, {1}, {2})'.format(mid, home_id, guest_id))
    except Exception as e:
        print(r, e)

# 需要解决双引号插入数据库的问题
for i in a:
    r = i[1][0][0]
    r = tr(str(i[1]).replace('None', ''))
    sql = 'insert into t_match values({0}, "{1}")'.format(i[0], r)
    try:
        cursor.execute(sql)
    except Exception as e:
        print(i[0], e, r)
        break;

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

cursor.close()
conn.commit()
conn.close()

doc = '''
    %Y  Year with century as a decimal number.
    %m  Month as a decimal number [01,12].
    %d  Day of the month as a decimal number [01,31].
    %H  Hour (24-hour clock) as a decimal number [00,23].
    %M  Minute as a decimal number [00,59].
    %S  Second as a decimal number [00,61].
    %z  Time zone offset from UTC.
    %a  Locale's abbreviated weekday name.
    %A  Locale's full weekday name.
    %b  Locale's abbreviated month name.
    %B  Locale's full month name.
    %c  Locale's appropriate date and time representation.
    %I  Hour (12-hour clock) as a decimal number [01,12].
    %p  Locale's equivalent of either AM or PM.
'''

time.strptime(r[4], '%d/%m/%Y %H:%M:%S')

c = [[[13,167,'Arsenal','Manchester City','08/10/2014 15:00:00','08/10/2014 00:00:00',6,'FT','2 : 0','3 : 0',None,None,'3 : 0'], [[[21,[['Santiago Cazorla','Jack Wilshere','goal','(1-0)',None,21,4522,42686]],[],1,0],[42,[['Aaron Ramsey','Yaya Sanogo','goal','(2-0)',None,42,26820,83304]],[],1,0],[45,[['Laurent Koscielny','Nacho Monreal','subst',None,None,45,30051,23072],['Yaya Sanogo','Olivier Giroud','subst',None,None,45,83304,24444],['Alexis Sánchez','Alex Oxlade-Chamberlain','subst',None,None,45,25244,84146]],[['Samir Nasri','David Silva','subst',None,None,45,13298,14102]],1,1],[51,[],[['Fernando',None,'yellow',None,None,51,31958,0]],0,1],[60,[['Olivier Giroud','Aaron Ramsey','goal','(3-0)',None,60,24444,26820]],[['Yaya Touré','Bruno Zuculini','subst',None,None,60,14053,125532],['Edin Dzeko','James Milner','subst',None,None,60,24845,4511]],1,1],[68,[['Jack Wilshere','Mathieu Flamini','subst',None,None,68,42686,6321]],[],1,0],[70,[['Santiago Cazorla','Tomas Rosicky','subst',None,None,70,4522,845]],[],1,0],[76,[],[['Aleksandar Kolarov','Micah Richards','subst',None,None,76,12267,14168]],0,1],[85,[],[['Jesús Navas','Scott Sinclair','subst',None,None,85,9446,12779]],0,1],[86,[['Aaron Ramsey','Joel Campbell','subst',None,None,86,26820,95977]],[],1,0]]], [[13,'Arsenal',7.25,[[['blocked_scoring_att',[3]],['att_goal_low_left',[1]],['accurate_pass',[341]],['att_goal_high_centre',[1]],['won_contest',[11]],['att_sv_high_centre',[1]],['ontarget_scoring_att',[4]],['total_scoring_att',[8]],['total_throws',[22]],['aerial_won',[12]],['total_pass',[428]],['goals',[3]],['att_miss_right',[1]],['total_tackle',[27]],['total_offside',[3]],['att_goal_low_right',[1]],['shot_off_target',[1]],['aerial_lost',[14]],['fk_foul_lost',[13]],['won_corners',[3]],['possession_percentage',[42.1]]]],[[73379,'Wojciech Szczesny',7.81,[[['accurate_pass',[19]],['touches',[46]],['saves',[1]],['aerial_won',[2]],['total_pass',[30]],['good_high_claim',[5]],['formation_place',[1]]]],1,'GK',1,0,0,'GK',24,196,84],[11367,'Mathieu Debuchy',8.03,[[['accurate_pass',[19]],['touches',[65]],['aerial_won',[1]],['total_pass',[30]],['total_tackle',[7]],['aerial_lost',[1]],['fouls',[1]],['formation_place',[2]]]],2,'DR',2,0,0,'D(R)',29,177,76],[124316,'Calum Chambers',8.33,[[['accurate_pass',[27]],['touches',[61]],['aerial_won',[1]],['total_pass',[34]],['last_man_tackle',[1]],['total_tackle',[2]],['aerial_lost',[2]],['fouls',[1]],['formation_place',[5]]]],2,'DC',21,0,0,'D(R)',19,183,66],[27550,'Kieran Gibbs',8.03,[[['blocked_scoring_att',[1]],['six_yard_block',[1]],['accurate_pass',[32]],['touches',[63]],['won_contest',[1]],['total_scoring_att',[1]],['aerial_won',[1]],['total_pass',[34]],['total_tackle',[2]],['fouls',[1]],['formation_place',[3]]]],2,'DL',3,0,0,'D(L)',25,178,70],[30051,'Laurent Koscielny',6.67,[[['accurate_pass',[21]],['touches',[27]],['total_pass',[21]],['total_tackle',[1]],['formation_place',[6]]]],2,'DC',6,1,45,'D(C)',29,186,75],[42686,'Jack Wilshere',7.36,[[['accurate_pass',[36]],['touches',[57]],['won_contest',[2]],['goal_assist',[1]],['total_pass',[41]],['aerial_lost',[3]],['formation_place',[10]]]],3,'MC',10,1,68,'M(CLR)',22,172,68],[26820,'Aaron Ramsey',8.84,[[['accurate_pass',[47]],['touches',[81]],['won_contest',[5]],['total_scoring_att',[1]],['goal_assist',[1]],['total_pass',[58]],['goals',[1]],['total_tackle',[4]],['fouls',[1]],['formation_place',[8]],['man_of_the_match',[1]]]],3,'MC',16,1,86,'M(CR)',23,177,70],[25244,'Alexis Sánchez',6.93,[[['accurate_pass',[15]],['touches',[39]],['won_contest',[3]],['total_pass',[25]],['fouls',[1]],['formation_place',[7]]]],3,'MR',17,1,45,'AM(CLR),FW',25,168,62],[4522,'Santiago Cazorla',8.1,[[['blocked_scoring_att',[1]],['accurate_pass',[30]],['touches',[53]],['total_scoring_att',[2]],['aerial_won',[1]],['total_pass',[35]],['goals',[1]],['total_tackle',[2]],['aerial_lost',[1]],['fouls',[1]],['formation_place',[11]]]],3,'ML',19,1,70,'M(CLR)',29,168,66],[1443,'Mikel Arteta',7,[[['accurate_pass',[45]],['touches',[59]],['total_pass',[52]],['total_tackle',[3]],['aerial_lost',[1]],['fouls',[3]],['formation_place',[4]]]],3,'DMC',8,0,0,'DM(C),M(L)',32,183,64],[83304,'Yaya Sanogo',7.48,[[['blocked_scoring_att',[1]],['accurate_pass',[9]],['touches',[20]],['total_scoring_att',[3]],['aerial_won',[3]],['goal_assist',[1]],['total_pass',[11]],['aerial_lost',[2]],['formation_place',[9]]]],4,'FW',22,1,45,'FW',21,191,74],[24444,'Olivier Giroud',7.55,[[['accurate_pass',[10]],['touches',[18]],['total_scoring_att',[1]],['aerial_won',[3]],['total_pass',[12]],['goals',[1]],['total_tackle',[2]],['aerial_lost',[1]],['fouls',[1]],['formation_place',[0]]]],5,'Sub',12,2,45,'FW',28,192,88],[84146,'Alex Oxlade-Chamberlain',6.5,[[['accurate_pass',[10]],['touches',[23]],['total_pass',[14]],['total_tackle',[2]],['aerial_lost',[1]],['formation_place',[0]]]],5,'Sub',15,2,45,'M(CLR)',21,180,70],[23072,'Nacho Monreal',6.68,[[['accurate_pass',[8]],['touches',[18]],['total_pass',[10]],['total_tackle',[2]],['aerial_lost',[1]],['formation_place',[0]]]],5,'Sub',18,2,45,'D(L)',28,178,72],[6321,'Mathieu Flamini',6.07,[[['accurate_pass',[8]],['touches',[16]],['total_pass',[13]],['fouls',[2]],['formation_place',[0]]]],5,'Sub',20,2,68,'DM(C)',30,178,67],[95977,'Joel Campbell',5.97,[[['touches',[1]],['total_pass',[1]],['fouls',[1]],['formation_place',[0]]]],5,'Sub',28,2,86,'AM(LR),FW',22,178,71],[102248,'Damián Martinez',0,[[['formation_place',[0]]]],5,'Sub',50,0,0,'GK',22,183,89],[845,'Tomas Rosicky',5.98,[[['accurate_pass',[5]],['touches',[7]],['total_pass',[7]],['aerial_lost',[1]],['formation_place',[0]]]],5,'Sub',7,2,70,'M(CLR)',34,178,65]],['4141',[[5,1],[8,3],[2,3],[5,5],[6,3],[4,3],[8,7],[6,7],[5,9],[4,7],[2,7]]]],[167,'Manchester City',6.28,[[['blocked_scoring_att',[5]],['accurate_pass',[500]],['att_miss_left',[1]],['won_contest',[11]],['ontarget_scoring_att',[1]],['total_scoring_att',[11]],['total_throws',[26]],['aerial_won',[14]],['total_pass',[588]],['att_miss_high_left',[1]],['att_miss_right',[1]],['post_scoring_att',[1]],['total_tackle',[19]],['att_sv_low_left',[1]],['shot_off_target',[5]],['aerial_lost',[12]],['fk_foul_lost',[15]],['won_corners',[7]],['possession_percentage',[57.9]],['att_post_left',[1]],['att_miss_high_right',[1]]]],[[34749,'Willy Caballero',5.45,[[['accurate_pass',[13]],['touches',[19]],['saves',[1]],['total_pass',[15]],['total_tackle',[1]],['formation_place',[1]]]],1,'GK',13,0,0,'GK',33,186,80],[12267,'Aleksandar Kolarov',5.94,[[['accurate_pass',[26]],['touches',[66]],['won_contest',[2]],['total_pass',[36]],['aerial_lost',[1]],['fouls',[3]],['formation_place',[3]]]],2,'DL',11,1,76,'D(L),M(L)',28,187,83],[6042,'Gaël Clichy',7.23,[[['accurate_pass',[53]],['touches',[112]],['won_contest',[2]],['total_scoring_att',[1]],['aerial_won',[2]],['total_pass',[75]],['total_tackle',[4]],['aerial_lost',[1]],['formation_place',[2]]]],2,'DR',22,0,0,'D(L)',29,176,65],[91200,'Matija Nastasic',6.47,[[['accurate_pass',[50]],['touches',[65]],['aerial_won',[1]],['total_pass',[52]],['aerial_lost',[4]],['fouls',[1]],['formation_place',[6]]]],2,'DC',33,0,0,'D(C)',21,187,79],[83032,'Dedryck Boyata',6.47,[[['accurate_pass',[49]],['touches',[65]],['won_contest',[1]],['total_scoring_att',[1]],['aerial_won',[3]],['total_pass',[51]],['total_tackle',[2]],['formation_place',[5]]]],2,'DC',38,0,0,'D(CR)',23,188,84],[9446,'Jesús Navas',6.52,[[['accurate_pass',[39]],['touches',[56]],['total_pass',[43]],['total_tackle',[3]],['aerial_lost',[1]],['fouls',[1]],['formation_place',[7]]]],3,'MR',15,1,85,'AM(CR)',28,170,60],[14053,'Yaya Touré',6.33,[[['accurate_pass',[47]],['touches',[61]],['total_pass',[54]],['total_tackle',[3]],['fouls',[2]],['formation_place',[4]]]],3,'MC',42,1,60,'M(C)',31,189,90],[31958,'Fernando',6.85,[[['blocked_scoring_att',[2]],['accurate_pass',[72]],['touches',[94]],['yellow_card',[1]],['won_contest',[3]],['total_scoring_att',[2]],['aerial_won',[2]],['total_pass',[78]],['total_tackle',[1]],['aerial_lost',[1]],['fouls',[4]],['formation_place',[8]]]],3,'MC',6,0,0,'DM(C)',27,183,76],[13298,'Samir Nasri',5.77,[[['blocked_scoring_att',[1]],['accurate_pass',[28]],['touches',[40]],['total_scoring_att',[1]],['total_pass',[31]],['formation_place',[11]]]],3,'ML',8,1,45,'AM(CLR)',27,175,75],[24845,'Edin Dzeko',6.12,[[['accurate_pass',[11]],['touches',[27]],['won_contest',[1]],['aerial_won',[3]],['total_pass',[16]],['formation_place',[9]]]],4,'FW',10,1,60,'FW',28,193,84],[29072,'Stevan Jovetic',6.87,[[['blocked_scoring_att',[1]],['accurate_pass',[37]],['touches',[63]],['won_contest',[2]],['total_scoring_att',[5]],['aerial_won',[2]],['total_pass',[44]],['post_scoring_att',[1]],['total_tackle',[2]],['aerial_lost',[1]],['fouls',[2]],['formation_place',[10]]]],4,'AMC',35,0,0,'AM(CL),FW',24,183,79],[8786,'Joe Hart',0,[[['formation_place',[0]]]],5,'Sub',1,0,0,'GK',27,196,91],[12779,'Scott Sinclair',6.12,[[['accurate_pass',[2]],['touches',[5]],['total_pass',[2]],['fouls',[1]],['formation_place',[0]]]],5,'Sub',12,2,85,'AM(L)',25,175,64],[106530,'Karim Rekik',0,[[['formation_place',[0]]]],5,'Sub',19,0,0,'D(C)',19,185,78],[14168,'Micah Richards',6.03,[[['accurate_pass',[12]],['touches',[14]],['total_pass',[13]],['formation_place',[0]]]],5,'Sub',2,2,76,'D(CR)',26,180,82],[14102,'David Silva',5.94,[[['accurate_pass',[27]],['touches',[44]],['total_pass',[35]],['total_tackle',[1]],['formation_place',[0]]]],5,'Sub',21,2,45,'AM(CLR)',28,170,67],[125532,'Bruno Zuculini',6.11,[[['accurate_pass',[23]],['touches',[30]],['aerial_won',[1]],['total_pass',[29]],['total_tackle',[1]],['aerial_lost',[2]],['fouls',[1]],['formation_place',[0]]]],5,'Sub',36,2,60,'M',21,178,72],[4511,'James Milner',6.19,[[['blocked_scoring_att',[1]],['accurate_pass',[11]],['touches',[25]],['total_scoring_att',[1]],['total_pass',[14]],['total_tackle',[1]],['aerial_lost',[1]],['formation_place',[0]]]],5,'Sub',7,2,60,'M(CLR)',28,175,70]],['4411',[[5,1],[2,3],[8,3],[4,5],[4,3],[6,3],[2,5],[6,5],[5,9],[5,7],[8,5]]]]]], 0]

#['create table t_team(id INTEGER PRIMARY KEY, name TEXT)', 'create table t_team_match(mid INTEGER, home_id INTEGER, guest_id INTEGER)', 'create table t_match(id INTEGER PRIMARY KEY,time INTEGER, statistics TEXT)']

t = time.strptime(r[4], '%d/%m/%Y %H:%M:%S')
t = time.mktime(time.localtime(time.mktime(t) + 8 * 60 * 60))
t = int(t)






#r = "[[[26, 24, 'Liverpool', 'Aston Villa', '09/13/2014 17:30:00', '09/13/2014 00:00:00', 6, 'FT', '0 : 1', '0 : 1', , , '0 : 1'], [[[9, [], [['Gabriel Agbonlahor', , 'goal', '(0-1)', , 9, 14036, 0]], 0, 1], [12, [['Adam Lallana', , 'yellow', , , 12, 21683, 0]], [], 1, 0], [61, [['Adam Lallana', 'Raheem Sterling', 'subst', , , 61, 21683, 97692]], [], 1, 0], [63, [], [['Alan Hutton', , 'yellow', , , 63, 6434, 0]], 0, 1], [71, [['Mario Balotelli', 'Rickie Lambert', 'subst', , , 71, 33799, 8409], ['Lazar Markovic', 'Fabio Borini', 'subst', , , 71, 105577, 80882]], [], 1, 0], [72, [], [['Andreas Weimann', \"Charles N'Zogbia\", 'subst', , , 72, 80719, 9743]], 0, 1], [76, [['Alberto Moreno', , 'yellow', , , 76, 113275, 0]], [], 1, 0], [86, [], [['Tom Cleverley', 'Carlos Sánchez', 'subst', , , 86, 69956, 26720]], 0, 1], [90, [], [['Gabriel Agbonlahor', 'Darren Bent', 'subst', , , 90, 14036, 3116]], 0, 1]]], [[26, 'Liverpool', 6.56272727272727, [[['blocked_scoring_att', [7]], ['accurate_pass', [659]], ['att_miss_left', [1]], ['won_contest', [2]], ['ontarget_scoring_att', [1]], ['total_scoring_att', [18]], ['total_throws', [22]], ['aerial_won', [23]], ['total_pass', [741]], ['att_miss_high_left', [1]], ['att_miss_right', [4]], ['post_scoring_att', [1]], ['total_tackle', [12]], ['total_offside', [3]], ['att_sv_low_left', [1]], ['shot_off_target', [10]], ['aerial_lost', [11]], ['fk_foul_lost', [9]], ['won_corners', [7]], ['possession_percentage', [74.7]], ['att_post_right', [1]], ['att_miss_high', [1]], ['att_miss_high_right', [2]]]], [[52197, 'Simon Mignolet', 6.02, [[['accurate_pass', [20]], ['touches', [28]], ['total_pass', [21]], ['good_high_claim', [1]], ['formation_place', [1]]]], 1, 'GK', 22, 0, 0, 'GK', 26, 193, 87], [29106, 'Dejan Lovren', 7.52, [[['blocked_scoring_att', [1]], ['accurate_pass', [100]], ['touches', [132]], ['total_scoring_att', [2]], ['aerial_won', [8]], ['total_pass', [115]], ['total_tackle', [3]], ['aerial_lost', [1]], ['fouls', [2]], ['formation_place', [5]]]], 2, 'DC', 6, 0, 0, 'D(C)', 25, 188, 84], [29575, 'Mamadou Sakho', 7.23, [[['accurate_pass', [94]], ['touches', [113]], ['total_scoring_att', [1]], ['aerial_won', [7]], ['total_pass', [101]], ['total_tackle', [1]], ['aerial_lost', [2]], ['formation_place', [6]]]], 2, 'DC', 17, 0, 0, 'D(C)', 24, 187, 83], [113275, 'Alberto Moreno', 6.39, [[['accurate_pass', [35]], ['touches', [59]], ['yellow_card', [1]], ['aerial_won', [2]], ['total_pass', [40]], ['fouls', [2]], ['formation_place', [3]]]], 2, 'DL', 18, 0, 0, 'D(L),M(L)', 22, 170, 65], [109227, 'Javier Manquillo', 7.06, [[['accurate_pass', [65]], ['touches', [104]], ['aerial_won', [2]], ['total_pass', [71]], ['total_tackle', [5]], ['formation_place', [2]]]], 2, 'DR', 19, 0, 0, 'D(R)', 20, 180, 76], [21683, 'Adam Lallana', 6.02, [[['blocked_scoring_att', [1]], ['accurate_pass', [16]], ['touches', [29]], ['yellow_card', [1]], ['total_scoring_att', [2]], ['total_pass', [20]], ['aerial_lost', [1]], ['fouls', [2]], ['formation_place', [11]]]], 3, 'AML', 20, 1, 61, 'AM(CLR)', 26, 173, 73], [68659, 'Jordan Henderson', 7, [[['accurate_pass', [111]], ['touches', [136]], ['total_scoring_att', [1]], ['aerial_won', [3]], ['total_pass', [121]], ['total_tackle', [2]], ['fouls', [2]], ['formation_place', [8]]]], 3, 'DMC', 14, 0, 0, 'M(CLR)', 24, 182, 67], [80767, 'Philippe Coutinho', 6.45, [[['blocked_scoring_att', [4]], ['accurate_pass', [60]], ['touches', [90]], ['total_scoring_att', [6]], ['total_pass', [71]], ['post_scoring_att', [1]], ['total_tackle', [1]], ['aerial_lost', [2]], ['formation_place', [10]]]], 3, 'AMC', 10, 0, 0, 'AM(CLR)', 22, 171, 71], [105577, 'Lazar Markovic', 5.97, [[['accurate_pass', [35]], ['touches', [56]], ['won_contest', [1]], ['total_scoring_att', [2]], ['total_pass', [41]], ['aerial_lost', [1]], ['formation_place', [7]]]], 3, 'AMR', 50, 1, 71, 'AM(LR)', 20, 175, 65], [17, 'Steven Gerrard', 6.73, [[['accurate_pass', [83]], ['touches', [107]], ['aerial_won', [1]], ['total_pass', [94]], ['aerial_lost', [1]], ['formation_place', [4]]]], 3, 'DMC', 8, 0, 0, 'M(C)', 34, 185, 82], [33799, 'Mario Balotelli', 6.09, [[['blocked_scoring_att', [1]], ['accurate_pass', [19]], ['touches', [28]], ['total_scoring_att', [2]], ['total_pass', [20]], ['aerial_lost', [1]], ['formation_place', [9]]]], 4, 'FW', 45, 1, 71, 'AM(LR),FW', 24, 189, 88], [31451, 'Lucas Leiva', 0, [[['formation_place', [0]]]], 5, 'Sub', 21, 0, 0, 'DM(C)', 27, 179, 74], [11774, 'Bradley Jones', 0, [[['formation_place', [0]]]], 5, 'Sub', 1, 0, 0, 'GK', 32, 191, 76], [3817, 'Kolo Touré', 0, [[['formation_place', [0]]]], 5, 'Sub', 4, 0, 0, 'D(C)', 33, 183, 74], [14230, 'José Enrique', 0, [[['formation_place', [0]]]], 5, 'Sub', 3, 0, 0, 'D(L),M(L)', 28, 184, 76], [80882, 'Fabio Borini', 5.79, [[['accurate_pass', [1]], ['touches', [5]], ['total_pass', [2]], ['aerial_lost', [2]], ['formation_place', [0]]]], 5, 'Sub', 29, 2, 71, 'AM(LR),FW', 23, 178, 73], [97692, 'Raheem Sterling', 6.16, [[['accurate_pass', [16]], ['touches', [28]], ['won_contest', [1]], ['total_scoring_att', [2]], ['total_pass', [20]], ['formation_place', [0]]]], 5, 'Sub', 31, 2, 61, 'AM(CLR)', 19, 170, 69], [8409, 'Rickie Lambert', 5.84, [[['accurate_pass', [4]], ['touches', [8]], ['total_pass', [4]], ['fouls', [1]], ['formation_place', [0]]]], 5, 'Sub', 9, 2, 71, 'FW', 32, 188, 77]], ['4231', [[5, 1], [8, 3], [2, 3], [4, 5], [6, 3], [4, 3], [7, 7], [6, 5], [5, 9], [5, 7], [3, 7]]]], [24, 'Aston Villa', 6.81727272727273, [[['blocked_scoring_att', [1]], ['accurate_pass', [151]], ['att_miss_left', [1]], ['won_contest', [1]], ['ontarget_scoring_att', [1]], ['total_scoring_att', [5]], ['total_throws', [25]], ['aerial_won', [11]], ['total_pass', [243]], ['goals', [1]], ['total_tackle', [13]], ['total_offside', [1]], ['att_goal_low_right', [1]], ['shot_off_target', [3]], ['aerial_lost', [23]], ['fk_foul_lost', [10]], ['won_corners', [6]], ['possession_percentage', [25.3]], ['att_miss_high_right', [2]]]], [[28746, 'Brad Guzan', 6.81, [[['accurate_pass', [7]], ['touches', [37]], ['saves', [1]], ['aerial_won', [1]], ['total_pass', [30]], ['good_high_claim', [1]], ['formation_place', [1]]]], 1, 'GK', 1, 0, 0, 'GK', 30, 193, 94], [35958, 'Aly Cissokho', 7.2, [[['accurate_pass', [10]], ['touches', [58]], ['total_pass', [23]], ['total_tackle', [4]], ['fouls', [1]], ['formation_place', [3]]]], 2, 'DL', 23, 0, 0, 'D(L)', 27, 181, 75], [42148, 'Nathan Baker', 7.75, [[['accurate_pass', [9]], ['touches', [34]], ['aerial_won', [2]], ['total_pass', [13]], ['total_tackle', [2]], ['aerial_lost', [2]], ['formation_place', [6]], ['man_of_the_match', [1]]]], 2, 'DC', 2, 0, 0, 'D(CL)', 23, 188, 75], [6434, 'Alan Hutton', 7.62, [[['accurate_pass', [15]], ['touches', [59]], ['yellow_card', [1]], ['aerial_won', [1]], ['total_pass', [23]], ['total_tackle', [1]], ['aerial_lost', [1]], ['fouls', [1]], ['formation_place', [2]]]], 2, 'DR', 21, 0, 0, 'D(R)', 29, 185, 72], [11234, 'Philippe Senderos', 7.13, [[['blocked_scoring_att', [1]], ['six_yard_block', [1]], ['accurate_pass', [8]], ['touches', [24]], ['total_scoring_att', [3]], ['aerial_won', [2]], ['total_pass', [11]], ['aerial_lost', [1]], ['fouls', [1]], ['formation_place', [5]]]], 2, 'DC', 14, 0, 0, 'D(C)', 29, 190, 84], [27213, 'Fabian Delph', 6.54, [[['accurate_pass', [24]], ['touches', [38]], ['total_pass', [31]], ['aerial_lost', [1]], ['formation_place', [8]]]], 3, 'MC', 16, 0, 0, 'DM(C)', 24, 174, 60], [69956, 'Tom Cleverley', 6.95, [[['accurate_pass', [16]], ['touches', [26]], ['aerial_won', [1]], ['total_pass', [18]], ['total_tackle', [2]], ['fouls', [1]], ['formation_place', [7]]]], 3, 'MC', 8, 1, 86, 'M(CLR)', 25, 175, 67], [79050, 'Ashley Westwood', 7.14, [[['accurate_pass', [16]], ['touches', [35]], ['aerial_won', [1]], ['total_pass', [22]], ['total_tackle', [1]], ['formation_place', [4]]]], 3, 'MC', 15, 0, 0, 'DM(C)', 24, 175, 67], [14036, 'Gabriel Agbonlahor', 7.14, [[['accurate_pass', [6]], ['touches', [23]], ['total_scoring_att', [1]], ['aerial_won', [2]], ['total_pass', [13]], ['goals', [1]], ['total_tackle', [1]], ['aerial_lost', [9]], ['fouls', [1]], ['formation_place', [10]]]], 4, 'FWR', 11, 1, 90, 'AM(LR),FW', 28, 178, 76], [80719, 'Andreas Weimann', 6.55, [[['accurate_pass', [15]], ['touches', [36]], ['won_contest', [1]], ['total_scoring_att', [1]], ['total_pass', [25]], ['aerial_lost', [4]], ['fouls', [2]], ['formation_place', [9]]]], 4, 'FW', 10, 1, 72, 'AM(CLR),FW', 23, 188, 76], [8058, 'Kieran Richardson', 6.32, [[['accurate_pass', [17]], ['touches', [31]], ['aerial_won', [1]], ['total_pass', [21]], ['total_tackle', [1]], ['aerial_lost', [2]], ['fouls', [2]], ['formation_place', [11]]]], 4, 'FWL', 18, 0, 0, 'D(L),M(CL)', 30, 173, 71], [79967, 'Leandro Bacuna', 0, [[['formation_place', [0]]]], 5, 'Sub', 7, 0, 0, 'D(R),M(R)', 23, 187, 77], [99901, 'Jores Okore', 0, [[['formation_place', [0]]]], 5, 'Sub', 5, 0, 0, 'D(C)', 22, 183, 80], [1034, 'Shay Given', 0, [[['formation_place', [0]]]], 5, 'Sub', 31, 0, 0, 'GK', 38, 183, 84], [113069, 'Jack Grealish', 0, [[['formation_place', [0]]]], 5, 'Sub', 40, 0, 0, 'M', 19, 178, 68], [3116, 'Darren Bent', 6.15, [[['touches', [1]], ['aerial_lost', [2]], ['formation_place', [0]]]], 5, 'Sub', 19, 2, 90, 'FW', 30, 180, 73], [26720, 'Carlos Sánchez', 6.26, [[['touches', [4]], ['total_pass', [1]], ['total_tackle', [1]], ['formation_place', [0]]]], 5, 'Sub', 24, 2, 86, 'DM(C)', 28, 182, 80], [9743, \"Charles N'Zogbia\", 6.07, [[['accurate_pass', [8]], ['touches', [17]], ['total_pass', [12]], ['aerial_lost', [1]], ['fouls', [1]], ['formation_place', [0]]]], 5, 'Sub', 28, 2, 72, 'AM(CLR)', 28, 170, 70]], ['433', [[5, 1], [2, 3], [8, 3], [5, 6], [4, 3], [6, 3], [3, 6], [7, 6], [5, 9], [3, 9], [7, 9]]]]]], 0]"
