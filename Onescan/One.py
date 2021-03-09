#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
import re
from module import color_one
from module import port_scan
from module import image_effect
from  module import d_scan
from JS import js_scan
from module import C_scan

# poc模块
from poc import CVE17519
from poc import thinkadmin
from poc import OA_ajax

def par():
    global args
    print('\n')
    parser = argparse.ArgumentParser()
    parser.usage = "One.py -u http://www.example.com/ -d dir -c ..."
    parser.add_argument('-u', action='store',help='指定url 或 ip                                  如:-u http://www.baidu.com')
    parser.add_argument('-c', default=False, action='store_true',help='C段扫描                                            ')
    parser.add_argument('-j',default=False, action='store_true', help='js接口扫描                                           ')
    parser.add_argument('-js', default=False, action='store_true',help=' js接口扫描深度探测                                           ')
    parser.add_argument('-d',action='store',help='目录扫描                                             如: -d dir')
    parser.add_argument('-p', default=False, action='store_true',help='默认的端口扫描')
    parser.add_argument('-P',  action='store', help='指定端口扫描 如 1-100,445')
    parser.add_argument('-poc',default=False,action='store_true',help='漏洞验证')
    parser.add_argument('-proxy', action='store', help='代理设置  例如:http://127.0.0.1:1080(只支持http)')
    args = parser.parse_args()



def values():
    try:
        global payload
        global url
        global port
        url = args.u

        #端口
        if args.p == True:
                port_scan.url_one = url
                port_scan.main()
        else:
            pass

        if args.P != None:
              port_scan.url_one = url
              port_scan.ARGS_PARAMETER = args.P
              port_scan.run()
        else:
            pass

        #目录扫描
        if args.d != None and args.proxy != None:
                d_scan.args_one = args.d
                d_scan.PROXY = str(args.proxy)
                d_scan.url_one = url
                d_scan.URL_one = url
                d_scan.main()
        elif args.d != None:
                d_scan.args_one = args.d
                d_scan.url_one = url
                d_scan.URL_one = url
                d_scan.main()
        else:
            pass

        #POC检测
        if args.poc == True:
            CVE17519.url = url
            CVE17519.verify()

            thinkadmin.url = url
            thinkadmin.main()

            OA_ajax.url = url
            OA_ajax.run()
        else:
            pass

        # JS扫描
        if args.j == True:
            js_scan.URL = url
            js_scan.main()
        elif args.js == True:
            js_scan.URL = url
            js_scan.run()
        else:
            pass

        #C段扫描
        if args.c == True:
            C_scan.url_one = url
            C_scan.run()
        else:
            pass



    except  Exception as e:
        print("出现错误:",e)



if __name__ == '__main__':
    print(image_effect.randomArt())
    par()
    try:
        if ( args.u and args.p or args.P or args.poc or args.c or args.d or args.j or args.js) != None:
                values()
        else:
            print(color_one.red + "\t\t\t\t\t\twarning请输入-h查看帮助信息" + color_one.end)
    except:
        pass