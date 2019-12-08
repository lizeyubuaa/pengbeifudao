from email.header import Header
from email.mime.text import MIMEText
from smtplib import SMTP_SSL

# 自己的服务器
smtp_server = 'smtp.qq.com'
port = 465
# 帐号密码
from_addr = 'jichang.zhao@qq.com'
passwd = 'jmxflofuugodbgga'
# 收件人的服务器
to_addr = 'python_sem@163.com'
# 邮件构造
message = MIMEText('明天中午12点在A939开会。务必准时参加。', 'plain', 'utf-8')
message['From'] = Header(from_addr, 'utf-8')
message['To'] = Header("现代程序设计", 'utf-8')
message['Subject'] = Header('会议通知', 'utf-8')

server = SMTP_SSL(smtp_server, port)
# 先登录
server.login(from_addr, passwd)
print('登录成功')
print("邮件开始发送")
# 支持群发
server.sendmail(from_addr, [to_addr], message.as_string())
server.quit()
print("邮件发送成功")
