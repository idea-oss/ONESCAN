from module import color_one

# poc模块
from poc import CVE17519
from poc import thinkadmin
from poc import OA_ajax
from poc import qizhi
from poc import mysql_CVE_2012_2122
def main(url):
    print(color_one.red + '[DEBUG' + color_one.yellow + 'POC检测中....' + color_one.end)
    print((
        f'{color_one.green}================================================================================================={color_one.end}'))
    print(color_one.blue + "CVE17519漏洞检测中" + color_one.end)
    CVE17519.url = url
    CVE17519.verify()

    print(color_one.blue + "Thinkadmin任意文件读取漏洞检测中" + color_one.end)
    thinkadmin.url = url
    thinkadmin.main()
    print(color_one.blue + 'OA登录绕过 任意文件上传漏洞检测中' + color_one.end)
    OA_ajax.url = url
    OA_ajax.run()

    print(color_one.blue + "齐治堡垒机漏洞检测" + color_one.end)
    qizhi.run(url)

    print(color_one.blue + "mysql CVE-2012-2122 漏洞检测" + color_one.end)
    mysql_CVE_2012_2122.url=url
    mysql_CVE_2012_2122.run()
