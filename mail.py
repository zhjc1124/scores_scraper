import smtplib
from email.mime.text import MIMEText
from email.header import Header


def sendmail(text, receivers):
    sender = 'sxtyliuchang@sohu.com'
    receivers = [receivers]

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(text, 'plain', 'utf-8')
    message['From'] = Header("Test", 'utf-8')
    message['To'] = Header("Test", 'utf-8')

    subject = 'Python 成绩推送'
    message['Subject'] = Header(subject, 'utf-8')

    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, receivers, message.as_string())


if __name__ == "__main__":
    sendmail('TEST', '601040231@qq.com')