# -*- coding: utf-8 -*-
# @Time    : 2019/4/5
# @Author  : Jeffrey
import requests
import time
import re
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81"
                  " Safari/537.36"
}


class Chaocuo:
    url = "http://24mail.chacuo.net/"

    def __init__(self):
        self.cookies = None
        self.mid = ""
        self.email = ""
        self.code = ""

    def _get_site_cookie(self):
        # 获取站内cookie
        self.cookies = requests.get(url=self.url, headers=HEADERS).cookies

    def get_email(self):
        # 获取一个邮箱地址
        self._get_site_cookie()
        data = {"data": "666", "type": "renew", "arg": "d=027168.com_f="}
        html = requests.post(url=self.url, data=data, cookies=self.cookies, headers=HEADERS)
        self.cookies = html.cookies
        email = eval(html.text)['data'][0] + "@027168.com"
        self.email = email
        print("成功拿到一个邮箱地址：{email}".format(email=email))
        return email

    def _get_mid(self):
        # 获取最新的邮件id
        time.sleep(3.5)
        data = {"data": self.email.split("@")[0], "type": "refresh", "arg": ""}
        html = requests.post(url=self.url, data=data, cookies=self.cookies, headers=HEADERS)
        try:
            mid = eval(html.text)['data'][0]['list'][0]['MID']
            self.mid = mid
            print("成功获取到邮件id：{mid}".format(mid=mid))
        except IndexError:
            print("邮件id获取失败，请手动重试")

    def get_data(self):
        # 获取邮件内容
        self._get_mid()
        arg = "f={mid}".format(mid=self.mid)
        data = {"data": self.email.split("@")[0], "type": "mailinfo", "arg": arg}
        html = requests.post(url=self.url, data=data, cookies=self.cookies, headers=HEADERS)
        code = re.search(r"<b>(.*?)<\\/b>", html.text.strip()).group(1)
        print("成功获取到验证码code：{code}".format(code=code))
        self.code = code
        return code


class Wiki:
    url = "https://wikicc.net/"

    def __init__(self, email):
        self.email = email
        self.cookies = None
        self.node_arg = []
        self.ssr = []
        self.urls = []

    def get_code(self):
        # 发送验证码到邮箱
        data = {"email": self.email}
        html = requests.post(url=self.url + "auth/send", data=data, headers=HEADERS)
        print(eval(html.text)['msg'])

    def register(self, code):
        # 注册账号：其账号密码昵称均为邮箱
        data = {
            "email": self.email,
            "name": self.email,
            "passwd": self.email,
            "repasswd": self.email,
            "code": "",
            "emailcode": code
        }
        html = requests.post(url=self.url + "auth/register", data=data, headers=HEADERS)
        print(eval(html.text)['msg'])

    def login(self):
        # 登录账号
        data = {
            "email": self.email,
            "passwd": self.email
        }
        html = requests.post(url=self.url + "auth/login", data=data, headers=HEADERS)
        self.cookies = html.cookies
        print(eval(html.text)['msg'])

    def _get_node_arg(self):
        html = requests.get(url=self.url + "user/node", cookies=self.cookies, headers=HEADERS)
        res = re.findall(r'<a href="javascript:void\(0\);" onClick="urlChange\((.*?)\)', html.text.strip())
        self.node_arg = res

    def get_node(self):
        # 获取节点列表
        self._get_node_arg()
        print("-" * 60)
        print("节点ssr地址列表：")
        for item in self.node_arg:
            time.sleep(3.5)
            item = item.split(",")
            url = self.url + "user/node/{0}?ismu={1}&relay_rule={2}".format(item[0][1:-1], item[1], item[2])
            # noinspection PyBroadException
            try:
                html = requests.get(url=url, cookies=self.cookies, headers=HEADERS)
                ss = re.search(r"var text_qrcode2 = '(.*?)'", html.text).group(1)
                print(ss)
                self.ssr.append(ss)
            except Exception:
                pass

    def get_urls(self):
        print("-" * 60)
        print("节点ssr二维码地址列表：")
        ssr_addr = ""
        for item in self.ssr:
            ssr_addr += item
            url = "https://cli.im/api/qrcode/code?text={text}".format(text=item)
            self.urls.append(url)
            print(url)
        self.copy_addr(ssr_addr)
        print("-" * 60)
        print("已成功将所有SSR地址复制到剪贴板，可通过批量导入ssr地址完成配置")

    @staticmethod
    def copy_addr(s):
        command = 'echo ' + s.strip() + '| clip'
        os.system(command)


cc = Chaocuo()
email = cc.get_email()
wiki = Wiki(email)
wiki.get_code()
code = cc.get_data()
wiki.register(code)
wiki.login()
wiki.get_node()
wiki.get_urls()
while True:
    input()
