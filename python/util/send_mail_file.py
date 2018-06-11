#-*-coding:utf-8-*-
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
import sys
from config import ParseConfigurationFile
# reload(sys)
# sys.setdefaultencoding('utf8')

class Send_Mail_file(object):
    def get_report_file(self,report_path):
        '''第三步：获取最新的测试报告'''
        lists = os.listdir(report_path)
        lists.sort(key=lambda fn: os.path.getmtime(os.path.join(report_path, fn)))
        print (u'最新测试生成的报告： ' + lists[-1])
        # 找到最新生成的报告文件
        report_file = os.path.join(report_path, lists[-1])
        return report_file

    def send_mail(self,sender, psw, receiver, smtpserver, report_file,port=None):
        '''第四步：发送最新的测试报告内容'''
        with open(report_file, "rb") as f:
            mail_body = f.read()
        # 定义邮件内容
        msg = MIMEMultipart()
        body = MIMEText(mail_body, _subtype='html', _charset='utf-8')
        msg['Subject'] = u"自动化测试报告"
        msg["from"] = sender
       # msg["to"] = ";".join(receiver)
        msg["to"] = receiver
        msg.attach(body)
        # 添加附件
        att = MIMEText(open(report_file, "rb").read(), "base64", "utf-8")
        att["Content-Type"] = "application/octet-stream"
        att["Content-Disposition"] = 'attachment; filename= "report.html"'
        msg.attach(att)

        if port != None:
            smtp = smtplib.SMTP_SSL(smtpserver, port)
        else:
            smtp = smtplib.SMTP()
            smtp.connect(smtpserver)

        # 用户名密码
        smtp.login(sender, psw)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
        print('test report email has send out !')




if __name__ == "__main__":

    cur_path = os.path.dirname(os.getcwd())
    report_path = os.path.join(cur_path, "report")  # 用例文件夹
    mail = Send_Mail_file()
    report_file = mail.get_report_file(report_path) # 3获取最新的测试报告
    pc = ParseConfigurationFile.ParseConfigfile()
    '''sender = readConfig.sender
    psw = readConfig.psw
    smtp_server = readConfig.smtp_server
    port = readConfig.port
    receiver = readConfig.receiver'''
    sender = pc.getOptionValue("email", "sender")
    psw = pc.getOptionValue("email", "psw")
    smtp_server = pc.getOptionValue("email", "smtp_server")
    port = pc.getOptionValue("email", "port")
    receiver = pc.getOptionValue("email", "receiver")

    mail.send_mail(sender, psw, receiver, smtp_server, report_file,port )  # 4最后一步发送报告