import urllib
import urllib.request
import http.cookiejar
import hashlib
import json
import time

# 函数获取身份信息列表[姓名,教学号,身份证]，返回成绩以字典形式返回
def get_score(stu_info):
    # 防反爬虫
    time.sleep(2)
    name = stu_info[0]
    tcode = stu_info[1]
    id = stu_info[2]
    print(name, tcode, id, end = '\t')
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
        print('连接错误')
        return({})
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
        print('连接错误')
        return({})
    raw_result = response.read().decode()

    # 分析结果
    result = json.loads(raw_result)['items']
    if not bool(result):
        print('密码错误')
        return({})
    # 将数据转换成字典
    scores_dict = {x['kcmc']: x['cj'] for x in result}
    #等价# get_cj = lambda x :(x['kcmc'],x['cj'])
         # scores_dict = dict(list(map(get_cj, result)))
    if '被屏蔽' in scores_dict.values():
        print('成绩被屏蔽')
        return({})
    print('获取成功')
    return(scores_dict)