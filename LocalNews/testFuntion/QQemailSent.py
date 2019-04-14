#!/user/bin/env python3

import smtplib
from email.mime.text import MIMEText

class EMail(object):
    def __init__(self):
        self.fromAdd = "1403459511@qq.com"  # 你的邮箱   发件地址
        # to_ = input('Please input Recipient:')  # 收件地址
        self.toAdd = "1403459511@qq.com"
        # subject = input('Please input title:')  # 邮件标题
        self.subject = "服务器 新闻爬虫运行终端报告"

        self.pwd = "urckpwbbgbeqhdec"  # 授权码  nkijfhnodibbiifb  smtp tmap


    def SendEmail(self, text):

        msg = MIMEText(text)
        msg["Subject"] = self.subject
        msg["From"] = self.fromAdd
        msg["To"] = self.toAdd
        try:
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            s.login(self.fromAdd, self.pwd)
            s.sendmail(self.fromAdd, self.toAdd, msg.as_string())
            s.quit()
            print("Success!")
        except smtplib.SMTPException:
            print('Falied!')


if __name__ == '__main__':
    # todo 这个后期后时间也修改成从config中抽取出账号和密码的配置，减少耦合性
    # text = input('Please input Content:')  # 邮件内容
    text = "😍成功了拉，以后自动检测后就可以定时的向手机汇报程序中断了的消息拉"
    email = EMail()

    email.SendEmail( text)
