# -*- coding: utf-8 -*-
# @Time    : 2019/4/5
# @Author  : Jeffrey
import json
import random
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


class Star:
    url = "https://my.staryun.pro/"

    def __init__(self):
        self.email = self.random_str(8) + "@163.com"
        self.password = self.random_str(8)
        self.cookies = None
        self.headers = self.get_headers()
        self.node_arg = []
        self.ssr = []
        self.urls = []

    def register(self):
        print(Color.blue("[提示] 正在准备节点..."))
        data = {
            "email": self.email,
            "name": self.random_str(7),
            "passwd": self.password,
            "repasswd": self.password,
            "wechat": str(self.random_num(9)),
            "imtype": 1,
            "code": "666"
        }
        requests.post(url=self.url + "auth/register", data=data, headers=self.headers, timeout=TIME_OUT)

    def login(self):
        data = {
            "email": self.email,
            "passwd": self.password,
            "code": ""
        }
        res = requests.post(url=self.url + "auth/login", data=data, headers=self.headers, timeout=TIME_OUT)
        self.cookies = res.cookies
        if json.loads(res.text)["msg"] == "登录成功":
            print("{tip} 正在获取节点列表...".format(tip=Color.green("[成功]")))
        else:
            print("{tip} 结束获取节点列表...".format(tip=Color.red("[失败]")))

    def _get_node_arg(self):
        html = requests.get(url=self.url + "user/node", cookies=self.cookies, headers=self.headers, timeout=TIME_OUT)
        res = re.findall(r'<a href="javascript:void\(0\);" onClick="urlChange\((.*?)\)', html.text.strip())
        self.node_arg = res

    def get_node(self):
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

    @staticmethod
    def random_str(n):
        ss = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        salt = ''
        for i in range(n):
            salt += random.choice(ss)
        return salt

    @staticmethod
    def random_num(n):
        nn = '123456789'
        salt = ''
        for i in range(n):
            salt += random.choice(nn)
        return salt

    @staticmethod
    def get_headers():
        index = random.randint(1, len(UA) - 1)
        headers = {
            "User-Agent": UA[index].strip()
        }
        return headers


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


def start():
    print("-" * 60)
    wiki = Star()
    wiki.register()
    wiki.login()
    wiki.get_node()
    wiki.get_urls()
    while True:
        input()


if __name__ == '__main__':
    init(autoreset=True)
    print(GITHUB_URL)
    start()
