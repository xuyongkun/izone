#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
"""
@File           :   loginbaidu.py
@Contact        :   xuyongkun22@163.com
@Modify Time    :   2019/4/24 17:07 
@Author         :   kenny
@Version        :   1.0
@Desciption     :   None
@License        :   (C)Copyright 2017-2019, kenny 
"""
import requests, time, random, base64, re, math, rsa
from bs4 import BeautifulSoup
from http import cookiejar
from subprocess import Popen  # 打开图片
import urllib3
from urllib3.connectionpool import InsecureRequestWarning
from wenku.mailspider import MailSpider
import os



"""
获取BaiDuID（http://yun.baidu.com/）
获取token（https://passport.baidu.com/v2/api/?getapi&tpl=netdisk&apiver=v3）
完成登录。如果cookie里有BDUSS登录成功。
好像如果要获取百度云数据还需要从其他链接更新cookie。
"""


#由于需要提交表单，而python3默认是不提交表单的，所以这时只需在代码中加上以下代码即可。
# ssl._create_default_https_context = ssl._create_unverified_context

URL_BAIDU_WENKU = "https://wenku.baidu.com/"
URL_BAIDU_INDEX = "https://www.baidu.com/"
URL_BAIDU_TOKEN = "https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3&tt=%s&class=login&gid=%s&loginversion=v4&logintype=dialogLogin&traceid=&callback=%s"
URL_BAIDU_LOGIN = "https://passport.baidu.com/v2/api/?login"
URL_BAIDU_PUBKEY = "https://passport.baidu.com/v2/getpublickey?token={}&tpl=mn&apiver=v3&tt={}&gid={}&callback={}"
URL_BAIDU_AUTH1 = "https://passport.baidu.com/v2/sapi/authwidgetverify?authtoken=%s&type=&jsonp=1&apiver=v3&verifychannel=&action=getapi&vcode=&questionAndAnswer=&needsid=&rsakey"
# 用于发送获取邮箱验证码的请求
URL_BAIDU_AUTH2 = "https://passport.baidu.com/v2/sapi/authwidgetverify?authtoken=%s&type=email&jsonp=1&apiver=v3&verifychannel=&action=send&vcode=&quest"
# 检测二维码的URL
URL_BAIDU_AUTH3 = "https://passport.baidu.com/v2/sapi/authwidgetverify?authtoken=%s&type=email&jsonp=1&apiver=v3&verifychannel=&action=check&vcode=%s"
headers = {
    "Host": "passport.baidu.com",
    "Referer": "https://www.baidu.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
}

# 文库请求头
wenku_headers = {
    "Host": "wenku.baidu.com",
    "Referer": "https://wenku.baidu.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
}


class LoginBaidu:

    # 登录，取到BUDUSS等
    def login_proxy(self, session, ltoken, lstr, traceid, tt, callback):
        URL_BAIBU_LOGIN_PROXY = 'https://passport.baidu.com/v2/?loginproxy&u=https://www.baidu.com/&tpl=mn&ltoken=%s&lstr=%s&client=&traceid=%s&actiontype=2&traceid=%s&apiver=v3&tt=%s&traceid=%s&callback=%s'
        login_proxy_url = URL_BAIBU_LOGIN_PROXY % (ltoken, lstr, traceid, traceid, tt, traceid, callback)
        resp = session.get(login_proxy_url, headers=headers, verify=False)
        if resp.status_code == 200:
            print('登录成功！')
            p2 = re.compile(r'[(](.*)[)]', re.S)  # 贪婪匹配
            resp_str = re.findall(p2, resp.content.decode('utf-8'))[0]
            resp_no = eval(resp_str)['errInfo']['no']
            return resp_no
        else:
            return -1

    """
    取得登陆验证
    """
    def get_session(self):
        # 忽略警告
        urllib3.disable_warnings(InsecureRequestWarning)
        session = requests.session()
        curPath = os.path.abspath(os.path.dirname(__file__))
        cookie_path = os.path.join(curPath, 'static\cookies\BaiDuCookies.txt')
        session.cookies = cookiejar.MozillaCookieJar(filename=cookie_path, )
        try:
            session.cookies.load(ignore_discard=True, ignore_expires=True)       # 加载cookies文件
        except:
            print("cookies未保存或cookies已过期")
            gid = self.get_gid()
            tt = self.get_tt()
            # 发送请求，以获取pubkey, key
            session.get(URL_BAIDU_LOGIN, headers=headers, verify=False)
            token = self.get_token(session)
            callback = self.get_callback()
            pubkey, key = self.get_pubkey(session, token, tt, gid, call_back=callback)
            account = "15601553721"
            password = "@kenny0202"
            postData = {
                'staticpage': 'https://www.baidu.com/cache/user/html/v3Jump.html',
                'charset': 'UTF-8',
                'token': token,
                'tpl': 'mn',
                'subpro': '',
                'apiver': 'v3',
                'tt': self.get_tt(),
                'codestring': '',
                'safeflg': '0',
                'u': 'https://www.baidu.com/',
                'isPhone': 'false',
                'detect': '1',
                'gid': gid,
                'quick_user': '0',
                'logintype': 'dialogLogin',
                'logLoginType': 'pc_loginDialog',
                'idc': '',
                'loginmerge': 'true',
                'splogin': 'rate',
                'username': account,
                'password': self.get_rsa_password(password, pubkey),  # 经过加密
                'mem_pass': 'on',
                'rsakey': key,
                'crypttype': '12',
                'ppui_logintime': str(int(self.get_tt()) - int(token_time)),
                'countrycode': '',
                'fp_uid': '',
                'fp_info': '',
                'loginversion': 'v4',
                'callback': self.get_callback()
            }
            # 发送请求， 以获取authtoken, lstr, ltoken, traceid, 参数
            response = session.post(URL_BAIDU_LOGIN, postData, headers=headers)
            authtoken = re.findall(r'&authtoken=(.*?)&', response.text)[0]
            lstr = re.findall(r'&lstr=(.*?)&', response.text)[0]
            ltoken = re.findall(r'&ltoken=(.*?)&', response.text)[0]
            traceid = re.findall(r'&traceid=(.*?)&', response.text)[0]
            # 如果存在codeString则获取验证码图片，再次请求
            codeString = re.findall(r'codeString=(.*?)&userName', response.text)[0]
            while codeString:
                print('需要输入验证码')
                # 获取图片，保存图片，输入图片验证码
                gif_url = "https://passport.baidu.com/cgi-bin/genimage?{}".format(codeString)
                gif = session.get(gif_url, headers=headers)
                with open("baidu.gif", "wb") as f:
                    f.write(gif.content)
                Popen("baidu.gif", shell=True)
                verifycode = input("验证码：")
                postData["verifycode"] = verifycode
                postData["codestring"] = codeString
                # 再次登录
                relogin = session.post(URL_BAIDU_LOGIN, postData, headers=headers)
                codeString = re.findall(r'codeString=(.*?)&userName', relogin.text)[0]

            self.getapi(session, authtoken)
            self.send_vcode(session, authtoken)
            # 发送验证码后等待5秒，保证邮箱收到验证码
            time.sleep(5)
            vcode = self.get_vcode()    # 该参数为手机验证码或邮箱验证码，或百度管家验证码
            # 验证邮箱验证码
            self.check_vcode(session, authtoken, vcode)
            # 登录
            ret = self.login_proxy(session, ltoken, lstr, traceid, self.get_tt(), self.get_callback())
            if '0' == ret:
                # 保存cookie, 下次可以使用cookie直接登录
                session.cookies.save(ignore_discard=True, ignore_expires=True)
            else:
                print('登录失败，请查找原因')

        # 验证是否登录成功
        # print(self.isLogin(session))
        return session

    # 判断是否已经登录
    def isLogin(self, session):
        response = session.get(URL_BAIDU_INDEX, headers=headers, verify=False)
        login_code = response.status_code
        if login_code == 200:
            return True
            print('登陆成功：')
        else:
            return False



    # 获取时间戳
    def get_tt(self):
        return int(round(time.time() * 1000))

    def get_idx(self, i):
        if i != 'x' and i != 'y':
            return i
        t = random.randint(0, 16)
        if 'x' == i:
            n = t
        else:
            n = (3 & t) if 3 & t else 8
        return hex(n).replace('0x', '')

    # 构造gid
    def get_gid(self):
        guide = [self.get_idx(i) for i in "xxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"]
        return "".join(guide).upper()

    # 随机生成callback
    def get_callback(self):
        prefix = "bd__cbs__"  # callback 前缀
        char = "0123456789abcdefghijklmnopqrstuvwxyz"
        n = random.randint(0, 2147483648)
        suffix = []
        while n != 0:
            suffix.append(char[n % 36])
            n = n // 36
        suffix.reverse()
        # print("callback: " + (prefix + ''.join(suffix)))
        return prefix + ''.join(suffix)

    # 获取token
    def get_token(self, session):
        global token_time
        token_time = self.get_tt()
        call_back = self.get_callback()
        gid = self.get_gid()
        get_token = URL_BAIDU_TOKEN % (token_time, gid, call_back)
        response = session.get(get_token, headers=headers, verify=False)
        token_all = response.text.replace(call_back, "")
        token_all = eval(token_all)
        return token_all["data"]["token"]

    def get_pubkey(self, session, token, tt, gid, call_back):
        # pubkey_callback = self.get_callback()
        pubkey_url = URL_BAIDU_PUBKEY.format(token, tt, gid, call_back)
        response = session.get(pubkey_url, headers=headers, verify=False)
        pubkey_all = eval(response.text.replace(call_back, ""))
        return pubkey_all["pubkey"], pubkey_all["key"]

    # 密码rsa加密
    def get_rsa_password(self, psw, pk):
        pub = rsa.PublicKey.load_pkcs1_openssl_pem(pk.encode("utf-8"))
        psw = psw.encode("utf-8")
        passwd = rsa.encrypt(psw, pub)
        passwd = base64.b64encode(passwd)
        return passwd.decode("utf-8")

    # 请求api地址， 模拟输入用户名密码后登录后的请求
    def getapi(self, session, authtoken):
        getapi_url = URL_BAIDU_AUTH1 % (authtoken)
        session.get(getapi_url, headers=headers, verify=False)

    # 模拟点击发送（邮箱）验证码请求
    def send_vcode(self, session, authtoken):
        send_vcode_url = URL_BAIDU_AUTH2 % (authtoken)
        session.get(send_vcode_url, headers=headers, verify=False)

    # 获取邮箱验证码
    def get_vcode(self):
        mailSpider = MailSpider()
        vcode = mailSpider.receive_mail_vcode()
        return vcode

    # 模拟输入验证码后，点击确定的按钮
    def check_vcode(self, session, aurhtoken, vcode):
        check_vcode_url = URL_BAIDU_AUTH3 % (aurhtoken, vcode)
        session.get(check_vcode_url, headers=headers, verify=False)

       # 获取文档id
    def get_doc_form(self, session, url):
        response = session.get(url, headers=wenku_headers, verify=False)
        # 这里请求后cookie 变了
        response.encoding = 'GBK'
        # print(response.text)
        return response.text

    # 获取ct
    def get_ct(self, soup):
        ct = soup.find('input', attrs={'name': 'ct'})['value']
        return ct

    # 获取doc_id
    def get_docid(self, soup):
        doc_id = soup.find('input', attrs={'name': 'doc_id'})['value']
        return doc_id

    def get_storage(self, soup):
        storage = soup.find('input', attrs={'name': 'storage'})['value']
        return storage

    def get_useTicket(self, soup):
        useTicket = soup.find('input', attrs={'name': 'useTicket'})['value']
        return useTicket

    def get_target_uticket_num(self, soup):
        target_uticket_num = soup.find('input', attrs={'name': 'target_uticket_num'})['value']
        return target_uticket_num

    def get_downloadToken(self, soup):
        downloadToken = soup.find('input', attrs={'name': 'downloadToken'})['value']
        return downloadToken

    def get_sz(self, soup):
        sz = soup.find('input', attrs={'name': 'sz'})['value']
        return sz

    def get_v_code(self, soup):
        v_code = soup.find('input', attrs={'name': 'v_code'})['value']
        return v_code

    def get_v_input(self,  soup):
        v_input = soup.find('input', attrs={'name': 'v_input'})['value']
        return v_input

    def get_req_vip_free_doc(self, soup):
        req_vip_free_doc = soup.find('input', attrs={'name': 'req_vip_free_doc'})['value']
        return req_vip_free_doc

    def get_retType(self, soup):
        retType = soup.find('input', attrs={'name': 'retType'})['value']
        return retType

    def get_sns_type(self, soup):
        sns_type = soup.find('input', attrs={'name': 'sns_type'})['value']
        return sns_type

    """
    下载文档，返回文档地址，该地址会在一段时间内有效
    """

    def download_document(self, session, url):
        download_url = 'https://wenku.baidu.com/user/submit/download'
        html_text = self.get_doc_form(session, url)
        download_headers = {
            "Host": "wenku.baidu.com",
            "Referer": url,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
            "Upgrade-Insecure-Requests": '1',
        }
        soup = BeautifulSoup(html_text, 'html.parser')
        param = {
            'ct': self.get_ct(soup),
            'doc_id': self.get_docid(soup),
            'retType': self.get_retType(soup),
            'sns_type': '',
            'storage': self.get_storage(soup),
            'useTicket': self.get_useTicket(soup),
            'target_uticket_num': self.get_target_uticket_num(soup),
            'downloadToken': self.get_downloadToken(soup),
            'sz': self.get_sz(soup),
            'v_code': self.get_v_code(soup),
            'v_input': self.get_v_input(soup),
            'req_vip_free_doc': self.get_req_vip_free_doc(soup)
        }
        # allow_redirects=False是必须的
        resp_dl = session.post(download_url, param, headers=download_headers, allow_redirects=False)
        # 获取响应头中的location
        doc_address = resp_dl.headers
        return doc_address['location']


    def test_cookie(self):
        from urllib import request
        # 声明一个CookieJar对象实例来保存cookie
        cookie = cookiejar.MozillaCookieJar()
        # 利用urllib库中的request的HTTPCookieProcessor对象来创建cookie处理器
        handler = request.HTTPCookieProcessor(cookie)
        # 通过handler来构建opener
        opener = request.build_opener(handler)
        # 此处的open方法同urllib的urlopen方法，也可以传入request
        response = opener.open('http://www.baidu.com')
        for item in cookie:
            print('Name = ' + item.name)
            print('Value = ' + item.value)



if __name__ == '__main__':
    login = LoginBaidu()
    # login.test_cookie()
    session = login.get_session()
    url = "https://wenku.baidu.com/view/0b1d6240be1e650e52ea991a.html"
    login.download_document(session, url)

