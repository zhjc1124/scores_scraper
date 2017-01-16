#将学生身份信息存储在数据库里

import pymysql.cursors

#登录信息都存在文件里防泄露
connect_data = open("user.txt",'r')
data = connect_data.read().split('\n')

#连接数据库
connections = pymysql.connect(host = data[0],user = data[1],password = data[2],charset = data[3])

#打开数据库指针
with connections.cursor() as cursor:
    #创建并使用shujukustu2016
    cursor.execute('create database stu2016 character set utf8;')
    cursor.execute('use stu2016')
    #创建表stu键分别对应姓名，教学号，身份证号
    cursor.execute('''create table stuall(name varchar(20) not null,
                                         tcode char(8) not null primary key,
                                         id char(18) not null);''')
    #打开存有学生信息的文件
    with open('stu.txt','r',encoding = 'utf8') as f:
         for line in f.readlines():
             cursor.execute('insert into stu values(%s,%s,%s);',tuple(line.strip().split('\t')))