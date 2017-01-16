
import pymysql.cursors

#登录信息都存在文件里防泄露
connect_data = open("user.txt",'r')
data = connect_data.read().split('\n')

#连接数据库
connections = pymysql.connect(host = data[0],user = data[1],password = data[2],charset = data[3])
with connections.cursor() as cursor:
    cursor.execute('use stu2016')
    cursor.execute('use stu2016')