
import pymysql.cursors

import urllib
import urllib.request
import http.cookiejar
import hashlib
import json
import time

NETERROR = []
PASSWORD_CHANGED = []
UNREGISTED = []
# 函数获取身份信息列表，返回成绩以['英语','大计基','工图','思修','c语言','高数']列表形式返回
def get_score(stu_info):
    time.sleep(2)
    global PASSWORD_CHANGED
    global UNREGISTED
    global NETERROR
    name = stu_info[0]
    tcode = stu_info[1]
    id = stu_info[2]

    #  账号密码赋值
    username = tcode                                                                             # 账号为教学号
    password = id[-6::].lower()                                                                  # 身份证最后六位为默认密码,最后一位为X的需要改成小写

    #  发送的postData中j_username直接就是账号,j_password是对应字符串的md5值
    j_username = username
    raw_j_password = 'UIMS' + username + password
    j_password = hashlib.md5(raw_j_password.encode()).hexdigest()
    post_data = {
        'j_username': j_username,
        'j_password': j_password,
    }
    post_data = urllib.parse.urlencode(post_data).encode()                                        # python2中为urllib.urlencode()

    # 模拟登陆cookies
    login_url = 'http://cjcx.jlu.edu.cn/score/action/security_check.php'
    cookie = http.cookiejar.MozillaCookieJar()                                                    # python2为cookielib.MozillaCookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))              # python2中urllib2在python3中为urllib.request
    try:
        result = opener.open(login_url, post_data)
    except Exception:
        NETERROR.append(username)
        return(stu_info + [-1] * 6)
    # post数据
    phpsession = list(cookie)[0].value
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '68',
        'Content-Type': 'application/json',
        'Cookie': 'JSESSIONID=; loginPage=userLogin.jsp; alu='+username+'; alp='+password+'; ald=month; PHPSESSID='+phpsession,
        'Host': 'cjcx.jlu.edu.cn',
        'Origin': 'http://cjcx.jlu.edu.cn',
        'Referer': 'http://cjcx.jlu.edu.cn/score/index.php',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'

    }
    post_url = 'http://cjcx.jlu.edu.cn/score/action/service_res.php'
    post_data = '{"tag":"lessonSelectResult@oldStudScore","params":{"xh":"' + username + '"}}'
    post_data = post_data.encode()
    # post_data = '{"tag":"lessonSelectResult@oldStudScore","params":{"xh":"' + username +'","termId":' + 131 + '}}'
                                                                                                # 131是2016-2017第一个学期，其他的按时间加1减1
    request = urllib.request.Request(post_url, post_data, headers)
    try:
        response = urllib.request.urlopen(request)
    except Exception:
        return(stu_info + [-1] * 6)
    raw_result = response.read().decode()

    # 分析结果
    result = json.loads(raw_result)['items']
    # 如果密码错误，result是空[]，把成绩设为-1，PASSWORD_CHANGED用来计数
    if not bool(result):
        PASSWORD_CHANGED.append(username)
        return(stu_info + [-1] * 6)
    # 将数据转换成字典
    get_cj = lambda x :(x['kcmc'],x['cj'])
    scores_dict = dict(list(map(get_cj, result)))
    #信息学生没有‘程序设计与编程’，设初值-1
    scores_dict.setdefault('程序设计与编程',-1)
    #英语分了一二级班。这里简化合并
    if '大学英语BⅡ' in scores_dict:
        scores_dict['大学英语BⅠ'] = scores_dict['大学英语BⅡ']
    get_list = ['大学英语BⅠ','大学计算机基础','工程图学D','思想道德修养与法律基础','程序设计与编程','高等数学BⅠ']
    scores_list = list( map( lambda x: scores_dict[x], get_list) )
    #被屏蔽进行计数
    if '被屏蔽' in scores_list:
        UNREGISTED.append(username)
        scores_list = [-1] * 6
    return(stu_info + scores_list)


#登录信息存在文件里防泄露
connect_data = open("user.txt",'r')
data = connect_data.read().split('\n')

#连接数据库
connections = pymysql.connect(host = data[0],user = data[1],password = data[2],charset = data[3])

#打开数据库指针
with connections.cursor() as cursor:
    #创建并使用数据库stu2016
    cursor.execute('create database stu2016 character set utf8;')
    cursor.execute('use stu2016')
    #创建表stu键，依次是姓名，教学号，身份证号，英语，大计基，工图，思修，c语言，高数
    cursor.execute('''create table stu(name varchar(20) not null,
                                         tcode char(8) not null primary key,
                                         id char(18) not null,
                                         english int not NULL,
                                         computer int not null,
                                         draw int not NULL,
                                         policy int not NULL,
                                         program int not NULL,
                                         math int not NULL);''')

    # 打开存有学生信息的文件
    with open('stu.txt', 'r', encoding='utf8') as f:
        stu_infos = f.readlines()
        ALL_STU = len(stu_infos)
        for line in stu_infos:
            stu_info = line.strip().split('\t')
            stu_scores = get_score(stu_info)
            print('总人数%s人' % ALL_STU, end='\t')
            print('密码错误%s个' % len(PASSWORD_CHANGED), end = '\t')
            print('被屏蔽%s个' % len(UNREGISTED), end='\t')
            print('网络错误%s个' % len(NETERROR), end='\t')
            for item in stu_scores:
                print(item, end = '\t')
            cursor.execute('insert into stu values(%s,%s,%s,%s,%s,%s,%s,%s,%s);', stu_scores)
            print('')

#打印错误信息和有关列表中的人
def print_summit(info,rel_list):
    print(info)
    for stu in rel_list:
        print(stu, end='\t')
list( map(print_summit, (('\n密码错误:', PASSWORD_CHANGED),
                         ('\n屏蔽错误:', UNREGISTED),
                         ('\n网络错误:', NETERROR)) ) )