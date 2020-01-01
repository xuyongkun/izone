#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
"""
@File           :   mailspider.py 
@Contact        :   xuyongkun22@163.com
@Modify Time    :   2019/5/19 14:28 
@Author         :   kenny
@Version        :   1.0
@Desciption     :   自动登录邮箱，并提取百度发送的验证码
@License        :   (C)Copyright 2017-2019, kenny 
"""
import requests
import urllib, urllib3
from bs4 import BeautifulSoup
from http import cookiejar
from urllib3.connectionpool import InsecureRequestWarning
import smtplib, imaplib


class MailSpider:

    def login(self):
        urllib3.disable_warnings(InsecureRequestWarning)
        session = requests.session()
        # 创建cookies
        session.cookies = cookiejar.LWPCookieJar()



    """
    import getpass, imaplib

    M = imaplib.IMAP4()
    M.login(getpass.getuser(), getpass.getpass())
    M.select()
    typ, data = M.search(None, 'ALL')
    for num in data[0].split():
        typ, data = M.fetch(num, '(RFC822)')
        print 'Message %s\n%s\n' % (num, data[0][1])
    M.close()
    M.logout()
    """

    def receive_mail_vcode(self):
        imap_host = "imap.sina.com"
        imap_post = "143"
        username = "kenny_baidu"
        password = "kenny0202"
        try:
            email_server = imaplib.IMAP4(host=imap_host, port=imap_post)
            print("imap4----connect server success, now will check username")
        except:
            print("imap4----sorry the given email server address connect time out")
        try:
            # 验证用户名和密码
            typ, dat = email_server.login(username, password)
            if typ == 'OK':
                print('登录成功......')
                print("imap4----username exist, now will check password")
            else:
                print('登录失败，请检查用户名和密码')
        except:
            print("imap4----sorry the given email address or password seem do not correct")

        email_server.select('INBOX', False)
        # 返回响应代码的数据
        data = email_server.search(None, 'ALL')[1][0].split()
        # 邮箱中其收到的邮件的数量
        mail_num = len(data)
        # 通过fetch(index)读取第index封邮件的内容；这里读取最后一封，也即最新收到的那一封邮件
        typ, email_content = email_server.fetch(f'{mail_num}'.encode(), '(RFC822)')
        # 将邮件内存由byte转成str
        email_content = email_content[0][1].decode()
        vcode = self.get_vcode(email_content)
        email_server.close()
        # 关闭连接
        email_server.logout()
        return vcode


    #解析email 内容，提取验证码
    def get_vcode(self, email_content):
        content = BeautifulSoup(email_content, 'html.parser')
        bstring = content.find_all('b')
        vcode = bstring[0].get_text()
        print('邮箱验证码：', vcode)
        return vcode






if __name__ == '__main__':
    mail = MailSpider()
    mail.receive_mail_vcode()