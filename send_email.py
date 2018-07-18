import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

FROM_NAME = 'HHH'  # 发件人名
FROM_EMAIL = 'someone@example.com'  # 发件邮箱
PASSWORD = 'xxxxxx'  # 发件邮箱密码
SMTP_SERVER = 'i_do_not_know'  # smtp服务器，Outlook邮箱是'smtp-mail.outlook.com'，其他自行百度


def send(mailto, change_grades, all_grades, name):
    try:
        from_name = FROM_NAME  # 发件人名
        from_addr = FROM_EMAIL  # 发件地址
        to_addr = mailto  # 收件地址
        subject = '您的成绩已更新！'  # 邮件主题
        # 邮件正文
        html = '<h2>%s同学：</h2>' % name
        html += '<p>就在刚刚，我们注意到在我们上次通知您之后，您的成绩已再次被更新</p><p>更新的部分：</p>'
        html += '<table><thead><tr>'
        html += '<td>课程号</td>'
        html += '<td>课程名</td>'
        html += '<td>课程属性</td>'
        html += '<td>成绩</td>'
        html += '</tr></thead><tbody>'
        for rows in change_grades:
            html += '<tr>'
            for col in rows:
                html += '<td>%s</td>' % col
            html += '</tr>'
        html += '</tbody></table>'
        html += '<p>全部成绩：</p>'
        html += '<table><thead><tr>'
        html += '<td>课程号</td>'
        html += '<td>课程名</td>'
        html += '<td>课程属性</td>'
        html += '<td>成绩</td>'
        html += '</tr></thead><tbody>'
        for rows in all_grades:
            html += '<tr>'
            for col in rows:
                html += '<td>%s</td>' % col
            html += '</tr>'
        html += '</tbody></table>'
        password = PASSWORD
        smtp_server = SMTP_SERVER  # 邮件服务器

        msg = MIMEMultipart('alternative')  # 创建邮件
        msg['From'] = formataddr((Header(from_name, 'utf-8').encode(), from_addr))  # 发件人
        msg['Subject'] = Header(subject, 'utf-8').encode()  # 主题

        # 构造正文
        msgHTML = MIMEText(html, 'html', 'utf-8')
        msg.attach(msgHTML)

        # 发送
        server = smtplib.SMTP(smtp_server, 587)
        server.starttls()
        server.set_debuglevel(False)
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
        return True
    except:
        return False
