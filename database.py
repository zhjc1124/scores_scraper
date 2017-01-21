
import pymysql.cursors
from cjcx import get_score


#登录信息存在文件里防泄露
connect_data = open("user.txt",'r')
data = connect_data.read().split('\n')

#连接数据库
connections = pymysql.connect(host = data[0],user = data[1],password = data[2],charset = data[3])

#打开数据库指针
with connections.cursor() as cursor:
    # 创建并使用数据库stu2016
    cursor.execute('create database stu2016 character set utf8;')
    cursor.execute('use stu2016')
    # 创建表stu键，依次是姓名，教学号，身份证号，英语，大计基，工图，思修，c语言，高数
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
        for line in stu_infos:
            stu_info = line.strip().split('\t')
            scores_dict = get_score(stu_info)
            # 信息学生没有‘程序设计与编程’，设初值-1，而且排除没有某科的情况
            scores_dict.setdefault('程序设计与编程', -1)

            # 要查询的成绩列表
            get_list = ['大学英语BⅠ', '大学计算机基础', '工程图学D', '思想道德修养与法律基础', '程序设计与编程', '高等数学BⅠ']
            # 避免没有这科成绩的错误，故设成-1
            list(map(lambda x: scores_dict.setdefault(x, -1), get_list))
            # 英语分了一二级班。这里简化合并
            if '大学英语BⅡ' in scores_dict:
                scores_dict['大学英语BⅠ'] = scores_dict['大学英语BⅡ']
            scores_list = list(map(lambda x: scores_dict[x], get_list))
            cursor.execute('insert into stu values(%s,%s,%s,%s,%s,%s,%s,%s,%s);', stu_info + scores_list)