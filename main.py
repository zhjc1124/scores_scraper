import importlib,sys
importlib.reload(sys)
import pymysql.cursors

#登录信息都存在文件里防泄露
connect_data = open("user.txt",'r')
data = connect_data.read().split('\n')

#连接数据库
connections = pymysql.connect(host = data[0],user = data[1],password = data[2],charset = data[3])
with connections.cursor() as cursor:
    cursor.execute('use stu2015')
    cursor.execute('select * from stu')
    for a in cursor.fetchall():
        for b in a:
            print(b)
    #cursor.execute('create table test0 (name char(8) not null)')
    # cursor.execute('SHOW FULL COLUMNS FROM stu')
    # for a in cursor.fetchall():
    #     print(a)