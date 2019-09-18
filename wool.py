# -*- coding: utf-8 -*-
# @Time    : 2019/4/5
# @Author  : Jeffrey
import random
import string
import requests
import time
import re
import os
from colorama import init, Fore

GITHUB_URL = "Github项目地址: https://github.com/YYJeffrey/wool"
UA = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36"
]
TRY_COUNT = 16  # 获取ID尝试次数
TIME_OUT = 30  # 请求超时时间


class Chaocuo:
    url = "http://24mail.chacuo.net/"
    count = 0

    def __init__(self):
        self.cookies = None
        self.headers = p.get_headers()
        self.mid = ""
        self.email = ""
        self.code = ""

    def _get_site_cookie(self):
        # 获取站内cookie
        html = requests.get(url=self.url, headers=self.headers, timeout=TIME_OUT)
        self.cookies = html.cookies

    def get_email(self):
        # 获取一个邮箱地址
        self._get_site_cookie()
        data = {"data": "666", "type": "renew", "arg": "d=027168.com_f="}
        html = requests.post(url=self.url, data=data, cookies=self.cookies, headers=self.headers, timeout=TIME_OUT)
        self.cookies = html.cookies
        email = eval(html.text)['data'][0] + "@027168.com"
        self.email = email
        print("{tip} 获取Email: {email}".format(tip=Color.green("[成功]"), email=email))
        return email

    def _get_mid(self):
        # 获取最新的邮件id
        time.sleep(2)
        data = {"data": self.email.split("@")[0], "type": "refresh", "arg": ""}
        html = requests.post(url=self.url, data=data, cookies=self.cookies, headers=self.headers, timeout=TIME_OUT)
        self.count += 1
        # noinspection PyBroadException
        try:
            mid = eval(html.text)['data'][0]['list'][0]['MID']
            self.mid = mid
            print("{tip} 获取Email ID: {mid}".format(tip=Color.green("[成功]"), mid=mid))
        except Exception:
            print("{tip} 第{count}次尝试获取Email ID，将会在尝试{try_count}次后重启程序"
                  .format(tip=Color.red("[失败]"), count=self.count, try_count=TRY_COUNT))
            if self.count < TRY_COUNT:
                self._get_mid()
            else:
                print("{tip} 正在重启程序...".format(tip=Color.blue("[提示]")))
                start()

    def get_data(self):
        # 获取邮件内容
        self._get_mid()
        arg = "f={mid}".format(mid=self.mid)
        data = {"data": self.email.split("@")[0], "type": "mailinfo", "arg": arg}
        html = requests.post(url=self.url, data=data, cookies=self.cookies, headers=self.headers, timeout=TIME_OUT)
        code = re.search(r"<b>(.*?)<\\/b>", html.text.strip()).group(1)
        print("{tip} 获取Code: {code}".format(tip=Color.green("[成功]"), code=code))
        self.code = code
        return code


class Guerrill:
    url = "https://www.guerrillamail.com/ajax.php"
    count = 0

    def __init__(self):
        self.session = None
        self.headers = p.get_headers()
        self.mid = ""
        self.email = ""
        self.code = ""

    def get_email(self):
        # 获取站内session
        data = {
            "email_user": ''.join(random.sample(string.ascii_letters + string.digits, 9)),
            "lang": "zh",
            "site": "guerrillamail.com",
            "in": " 设置 取消"
        }
        session = requests.session()
        res = session.post(url=self.url + "?f=set_email_user", data=data, headers=self.headers, timeout=TIME_OUT)
        email = re.search(r'"email_addr":"(.*?)"', res.text.strip()).group(1)
        print("{tip} 获取Email: {email}".format(tip=Color.green("[成功]"), email=email))
        self.session = session
        self.email = email
        return email

    def _get_mid(self):
        # 获取最新的邮件id
        time.sleep(2)
        url = self.url + "?f=get_email_list&offset=0&site=guerrillamail.com&in={0}&_={1}" \
            .format(self.email.split("@")[0], int(round(time.time() * 1000)))
        res = self.session.get(url=url, headers=self.headers, timeout=TIME_OUT)
        self.count += 1
        # noinspection PyBroadException
        try:
            mid = re.search(r'{"list":\[{"mail_id":"(.*?)"', res.text.strip()).group(1)
            self.mid = mid
            print("{tip} 获取Email ID: {mid}".format(tip=Color.green("[成功]"), mid=mid))
        except Exception:
            print("{tip} 第{count}次尝试获取Email ID，将会在尝试{try_count}次后重启程序"
                  .format(tip=Color.red("[失败]"), count=self.count, try_count=TRY_COUNT))
            if self.count < TRY_COUNT:
                self._get_mid()
            else:
                print("{tip} 正在重启程序...".format(tip=Color.blue("[提示]")))
                start()

    def get_data(self):
        # 获取邮件内容
        self._get_mid()
        url = self.url + "?f=fetch_email&email_id=mr_{0}&site=guerrillamail.com&in={1}&_={2}" \
            .format(self.mid, self.email.split("@")[0], int(round(time.time() * 1000)))
        res = self.session.get(url=url, headers=self.headers, timeout=TIME_OUT)
        code = re.search(r"<b>(.*?)<\\/b>", res.text.strip()).group(1)
        print("{tip} 获取Code: {code}".format(tip=Color.green("[成功]"), code=code))
        self.code = code
        return code


class Wiki:
    url = "https://vvoo.in/"

    def __init__(self, email):
        self.email = email
        self.cookies = None
        self.headers = p.get_headers()
        self.node_arg = []
        self.ssr = []
        self.urls = []

    def get_code(self):
        # 发送验证码到邮箱
        data = {"email": self.email}
        requests.post(url=self.url + "auth/send", data=data, headers=self.headers, timeout=TIME_OUT)
        print(Color.blue("[提示] 正在准备Email ID..."))

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
        requests.post(url=self.url + "auth/register", data=data, headers=self.headers, timeout=TIME_OUT)
        print(Color.blue("[提示] 正在准备节点..."))

    def login(self):
        # 登录账号
        data = {
            "email": self.email,
            "passwd": self.email
        }
        html = requests.post(url=self.url + "auth/login", data=data, headers=self.headers, timeout=TIME_OUT)
        self.cookies = html.cookies
        if eval(html.text)['msg'].strip() == "欢迎回来":
            print("{tip} 正在获取节点列表...".format(tip=Color.green("[成功]")))
        else:
            print("{tip} 结束获取节点列表...".format(tip=Color.red("[失败]")))

    def _get_node_arg(self):
        html = requests.get(url=self.url + "user/node", cookies=self.cookies, headers=self.headers, timeout=TIME_OUT)
        res = re.findall(r'<a href="javascript:void\(0\);" onClick="urlChange\((.*?)\)', html.text.strip())
        self.node_arg = res

    def get_node(self):
        # 获取节点列表
        self._get_node_arg()
        print("-" * 60)
        print("节点SSR地址列表：")
        for item in self.node_arg:
            time.sleep(2)
            item = item.split(",")
            url = self.url + "user/node/{0}?ismu={1}&relay_rule={2}".format(item[0][1:-1], item[1], item[2])
            # noinspection PyBroadException
            try:
                html = requests.get(url=url, cookies=self.cookies, headers=self.headers, timeout=TIME_OUT)
                ss = re.search(r"var text_qrcode2 = '(.*?)'", html.text).group(1)
                print(ss)
                self.ssr.append(ss)
            except Exception:
                pass

    def get_urls(self):
        print("-" * 60)
        print("节点SSR二维码列表：")
        ssr_addr = ""
        for item in self.ssr[::-1]:
            ssr_addr += item
            url = "https://cli.im/api/qrcode/code?text={text}".format(text=item)
            self.urls.append(url)
            print(url)
        self.copy_addr(ssr_addr)
        print("-" * 60)
        print(Color.green("已将所有SSR地址复制到剪贴板，可通过剪贴板批量导入SSR地址完成配置"))

    @staticmethod
    def copy_addr(s):
        command = 'echo ' + s.strip() + '| clip'
        os.system(command)


class VVoo(Wiki):
    url = "https://vvoo.in/"

    def login(self):
        # 登录账号
        data = {
            "email": self.email,
            "passwd": self.email
        }
        html = requests.post(url=self.url + "auth/login", data=data, headers=self.headers, timeout=TIME_OUT)
        self.cookies = html.cookies
        if eval(html.text)['msg'].strip() == "登录成功":
            print("{tip} 正在获取节点列表...".format(tip=Color.green("[成功]")))
        else:
            print("{tip} 结束获取节点列表...".format(tip=Color.red("[失败]")))

    def _get_node_arg(self):
        html = requests.get(url=self.url + "user/node", cookies=self.cookies, headers=self.headers, timeout=TIME_OUT)
        res = re.findall(r'onClick="urlChange\((.*?)\)', html.text.strip())
        self.node_arg = res[0:int(len(res) / 2)]

    def get_urls(self):
        print("-" * 60)
        print("节点SSR二维码列表：")
        ssr_addr = ""
        for item in self.ssr[::-1]:
            ssr_addr += item
            url = "https://cli.im/api/qrcode/code?text={text}".format(text=item)
            self.urls.append(url)
            print(url)
        self.copy_addr(ssr_addr)
        print("-" * 60)
        print(Color.green("已将所有SSR地址复制到剪贴板，可通过剪贴板批量导入SSR地址完成配置"))


class Color:
    @staticmethod
    def red(s):
        return Fore.RED + s + Fore.RESET

    @staticmethod
    def green(s):
        return Fore.GREEN + s + Fore.RESET

    @staticmethod
    def blue(s):
        return Fore.BLUE + s + Fore.RESET

    @staticmethod
    def white(s):
        return Fore.WHITE + s + Fore.RESET


class ProxyRandom:
    def __init__(self):
        self.ua = UA

    def get_headers(self):
        index = random.randint(1, len(self.ua) - 1)
        headers = {
            "User-Agent": self.ua[index].strip()
        }
        return headers


def start():
    print("-" * 60)
    cc = Guerrill()
    email = cc.get_email()
    wiki = VVoo(email)
    wiki.get_code()
    code = cc.get_data()
    wiki.register(code)
    wiki.login()
    wiki.get_node()
    wiki.get_urls()
    while True:
        input()


if __name__ == '__main__':
    init(autoreset=True)
    print(GITHUB_URL)
    p = ProxyRandom()
    start()
