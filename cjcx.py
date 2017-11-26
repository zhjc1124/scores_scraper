import requests
import hashlib
import json
import time


# 函数获取身份信息列表[教学号密码]，返回成绩以字典形式返回
def get_score(username, password):
    # 新建session会话
    s = requests.session()

    #  发送的postData中j_username直接就是账号,j_password是对应字符串的md5值
    j_username = username
    raw_j_password = 'UIMS' + username + password
    j_password = hashlib.md5(raw_j_password.encode()).hexdigest()
    post_data = {
        'j_username': j_username,
        'j_password': j_password,
    }

    login_url = 'http://cjcx.jlu.edu.cn/score/action/security_check.php'

    # 模拟登陆
    s.post(login_url, data=post_data)

    post_url = 'http://cjcx.jlu.edu.cn/score/action/service_res.php'
    post_data = '{"tag":"lessonSelectResult@oldStudScore","params":{"xh":"' + username + '"}}'
    # 查询成绩
    response = s.post(post_url, data=post_data)

    result = json.loads(response.text)['items']
    scores_dict = {x['kcmc']: x['cj'] for x in result}
    print(scores_dict)
    return scores_dict


if __name__ == "__main__":
    username = input('请输入用户名：')
    password = input('请输入密码：')
    get_score(username, password)