#!/usr/bin/env python3
# encoding:utf8
import socket
import re
import aiohttp
import configparser
from netaddr import IPNetwork
import asyncio
from bs4 import BeautifulSoup
from module import color_one
from module import user_agent
from alive_progress import  alive_bar

url_one=''
ASYNCIO_COUNT=0
SELECTION_CODE = 0
TIMEOUT_SOCKET = 0
TIMEOUT_REQUESTS = 0
COUNT = 0
config = configparser.ConfigParser()
def READ_CONFIG_FILE():
    global ASYNCIO_COUNT
    global SELECTION_CODE
    global TIMEOUT_SOCKET
    global TIMEOUT_REQUESTS
    config.read('./config/conf.conf',encoding='utf-8')
    ASYNCIO_COUNT = config['limit_asyncio'].getint('limit_count')
    SELECTION_CODE = config['selec_c'].getint('code')
    TIMEOUT_SOCKET = config['time_out_socket'].getfloat('time_out_socket')
    TIMEOUT_REQUESTS = config['time_out_requests'].getfloat('time_out_requests')



Ports = []
Ports_other=[]

def read_port():
    with open("./dict/C_port.txt") as file:
        for port in file:
            Ports.append(port.strip('\n'))
    with open("./dict/C_other_port.txt") as other_file:
        for other_port in other_file:
            Ports_other.append(other_port.strip("\n"))

async  def get_info(url, client):
    global response
    response = None
    try:
         async with client.get(url=url, headers=user_agent.user_agent(), ssl=False) as response:
            if response.status == SELECTION_CODE:
                    pass
            elif response.status == 200:
                info_code = color_one.green + str(response.status) + color_one.end
            else:
                info_code = color_one.red + str(response.status) + color_one.end
            soup = BeautifulSoup(await response.text(), 'lxml')
            if soup != None:
                info_title = '[' + color_one.green_blue + soup.title.string.replace('\n', '').replace('\r', '').replace('\t',
                    '') + color_one.end + ']' if soup.title else ' '
            else:
                info_title = None
            info_len = '['+color_one.green + str(response.content_length) + color_one.end+']'
            if 'Server' in response.headers:
                info_server =  '['+color_one.yellow + response.headers['Server']+']' +color_one.end
                info_server += color_one.yellow+"[" + response.headers['X-Powered-By'] + color_one.end + "]" if 'X-Powered-By' in response.headers else "  "
            else:
                info_server = " "
            response.close()
            return ' '+ info_code + '\t\t' + info_title + info_server+ info_len


    except Exception:
        if response != None:
                response.close()
        return " " + color_one.green + "open" + color_one.end + " "


def url_to_ip(url):
    domain = url.split('/')[0] if '://' not in url else url.split('//')[1].split('/')[0]
    domain = domain.split(':')[0] if ':' in domain else domain
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except Exception as e:
        return False

async def connet(ip, sem,bar,client):
    global COUNT
    global writer
    writer = None
    async with sem:
        for port in Ports:
            bar()
            try:
                fut = asyncio.open_connection(ip, int(port))
                reader, writer = await asyncio.wait_for(fut, timeout=TIMEOUT_SOCKET)
                if writer != None:
                        if port in Ports_other:
                            url = str(ip) + ":" + str(port)
                            info = " " + color_one.green + "open" + color_one.end + " "
                        else:
                            protocol = "http" if port not in [443, 8443] else "https"
                            url = "{0}://{1}:{2}".format(protocol, ip, port)
                            info = await  get_info(url, client)

                        url= color_one.good+color_one.blue + url + color_one.end
                        print("%-28s %-28s\n" % (url, info))
                        COUNT += 1
                writer.close()

            except Exception as e:
                    if writer != None:
                        writer.close()

async def scan(ASYNCIO_COUNT,url):
    url1=url+'/24'
    sem = asyncio.Semaphore(ASYNCIO_COUNT)
    tasks = []
    cookie_jar_one = aiohttp.CookieJar(unsafe=True)
    timeout = aiohttp.ClientTimeout(total=15)
    try:
        if url1:
            ips = [str(ip) for ip in IPNetwork(url1)]
            with alive_bar() as bar:
                async with aiohttp.ClientSession(cookie_jar=cookie_jar_one, timeout=timeout) as client:
                    for ip in ips:
                        tasks.append(asyncio.create_task(connet(ip, sem,bar,client)))

                    await asyncio.wait(tasks)
    except:
        return None
    print(color_one.blue + "\nFound {0}\n".format(COUNT))

#主机识别
def Host_identification(URL):
    global url_one
    if re.search(r'http://',URL) or re.search(r'https://',URL):
           url_one = url_to_ip(URL)
           return url_one

    elif re.search(r'^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}',URL):
            return url_one

    else:
        print(color_one.red + '错误的地址' + color_one.end)

def main(url):
    global Ports
    if url:
        print(color_one.red+'[DEBUG'+color_one.yellow+'C段探测中....'+color_one.end)
        print((f'{color_one.green}================================================================================================={color_one.end}'))
        print(color_one.yellow + 'Target: ' + color_one.blue + url  + color_one.end + '\n')
        print(color_one.green_blue+'URL\t\t\t\t\t'+color_one.green_blue+'状态'+color_one.green_blue+
              '\t\t\t\t\tBanner\t\t\t\t\t'+color_one.end)
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(scan(ASYNCIO_COUNT,url))
        except KeyboardInterrupt:
            print(color_one.red + "\nCTRL+C detected, Exit..." + color_one.end)
def run():
    # 加载配置文件
    READ_CONFIG_FILE()
    read_port()
    url=Host_identification(url_one)
    if url != False:
        main(url)
