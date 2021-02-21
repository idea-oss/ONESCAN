#!/usr/bin/env python3
# encoding:utf8

import aiohttp
import asyncio
import configparser
from bs4 import BeautifulSoup
from alive_progress import alive_bar
from module import color_one
from module import user_agent
import selectors
import socket
import re

socket.setdefaulttimeout(20)
url_one = ''
URL_one=''
PROXY = None
args_one = ''
LIMIT_BYTE=0
TIMEOUT=0
PATH_BASIS_LOWER = './dict/d_scan_dict/dict/'
PATH_BASIS_UPPER = './dict/d_scan_dict/'
CONFING_READ=configparser.ConfigParser()

#green title content identify
TITLE_COUNT_TOTAL = []

#red title content identify
TITLE_COUNT_TOTATL_RED = []
#script title content identify
TITLE_COUNT_SCRIPT = []
TITLE_COUNT_ERROR = []

#match rules + content identify limit
match_rules_list = []

#limit asyncio count
ASYNCIO_COUNT = 200

#PAGE REPEAT COUNT
PAGE_REPEAT = 0

_PATH_URL=''

#display count
DISPLAY_COUNT = 0

#URL_PATH
def PATH_URL():
    global _PATH_URL
    reobj = re.compile(r'''(?xi)\A
    # Skip over scheme and authority, if any
    ([a-z][a-z0-9+\-.]*:(//[^/?#]+)?)?
    # Path
    ([a-z0-9\-._~%!$&'()*+,;=:@/]*)''')

    match = reobj.search(URL_one)
    if match and match.group(3) != '/':
        _PATH_URL = match.group(3)
    else:
        pass



def URL_one_display():
    global URL_one
    if URL_one.endswith('/'):
        URL_one = URL_one[0:-1]
    else:
        pass


def READ_FILE_TOTAL_LOWER(DIR_PATH):
        global URL_one
        global PAYLOAD_LIST_DISPLAY
        COUNT = 0
        PAYLOAD_LIST = []
        PATH_DIR = (PATH_BASIS_LOWER+DIR_PATH).strip('\n')

        PAYLOAD_LIST,COUNT = FILE_READ_TOTAL(PATH_DIR)
        return PAYLOAD_LIST,COUNT


def READ_FILE_TOTAL_UPPER(DIR_PATH_UPPER):
        global  URL_one
        global PAYLOAD_LIST_DISPLAY
        COUNT_UPPER = 0
        PAYLOAD_LIST_UPPER = []
        PATH_DIR_UPPER = (PATH_BASIS_UPPER+DIR_PATH_UPPER).strip('\n')
        PAYLOAD_LIST_UPPER, COUNT_UPPER = FILE_READ_TOTAL(PATH_DIR_UPPER)
        return PAYLOAD_LIST_UPPER,COUNT_UPPER



def Host_identification(URL_ONE):
    global url_one
    if re.search(r'http://',URL_ONE) or re.search(r'https://',URL_ONE):
           return URL_ONE

    elif re.search(r'^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}',url_one):
            if re.search(r'https://',URL_one):
                url_one = 'https://' + URL_ONE
            elif re.search(r'http://',URL_one):
                url_one = 'http://'+URL_ONE
            return url_one

    else:
        print(color_one.red + '错误的地址' + color_one.end)
        return False


def url_to_ip(url):
    global url_one
    domain = url.split('/')[0] if '://' not in url else url.split('//')[1].split('/')[0]
    domain = domain.split(':')[0] if ':' in domain else domain
    try:

        url_one = socket.gethostbyname(domain)
    except Exception as error:
        pass


#file read
def FILE_READ_TOTAL(PATH_ONE):
    COUNT_FILE_TOTAL = 0
    PAYLOAD_LIST_TOTAL_FILE=[]
    if _PATH_URL != None:
        with open(PATH_ONE) as file_one:
            for payload_one in file_one:
                COUNT_FILE_TOTAL += 1
                payload_one.split('\n')
                if payload_one.startswith('//'):
                    payload_one = payload_one.replace('//', '/')
                if payload_one.endswith('//'):
                    payload_one = payload_one.replace('//', '/')
                if payload_one.startswith('/'):
                    pass
                else:
                    payload_one = '/' + payload_one
                PAYLOAD_LIST_TOTAL_FILE.append(_PATH_URL+payload_one.strip('\n'))

    else:

        with open(PATH_ONE) as file_one:
            for payload_one in file_one:
                COUNT_FILE_TOTAL += 1
                payload_one.split('\n')
                if payload_one.startswith('//'):
                    payload_one = payload_one.replace('//', '/')
                if payload_one.endswith('//'):
                    payload_one = payload_one.replace('//', '/')
                if payload_one.startswith('/'):
                    pass

                else:
                    payload_one = '/' + payload_one

                PAYLOAD_LIST_TOTAL_FILE.append(payload_one.strip('\n'))

    return PAYLOAD_LIST_TOTAL_FILE,COUNT_FILE_TOTAL


async  def CODE_SCAN(payload,responese):
            CODE_ONE = int(responese.status)
            if CODE_ONE == 200:
               await CODE_200(payload,responese,CODE_ONE)

            elif CODE_ONE == 403 or CODE_ONE == 400:
                await  CODE_400(payload,responese,CODE_ONE)

            elif CODE_ONE == 302:
                await  CODE_302(payload,responese,CODE_ONE)

            elif CODE_ONE == 500 or CODE_ONE == 501 or CODE_ONE ==502 or CODE_ONE == 503 or CODE_ONE == 504:
                return False
            elif CODE_ONE == 404:
                return False
            else:
                await CODE_Other(payload, responese, CODE_ONE)

#200 TOTAL
async def CODE_200(payload,response,status_code):
        info_200 = color_one.green + '[' + str(status_code) + ']'+ color_one.end
        info_type = str(response.content_type)
        INFO_TYPE = color_one.green_blue + '[' + str(info_type) + ']' + color_one.end
        info_server_200 = color_one.good + color_one.green+ URL_one + payload + color_one.end
        if info_type == 'text/html':

            title_content = await title_Identify(response)
            TITLE_CONTENT =  '[' + title_content + ']'
            title_rules = await re_tilte_rules(response, title_content)
            TITLE_RULES = color_one.yellow + '[' +  str(title_rules) + ']' + color_one.end
            if title_content == 'title请求错误' and  title_rules == None:

                    TITLE_COUNT_TOTAL.append(title_content)
            elif title_content == 'title请求错误' or  title_content == None:
                    pass
            elif title_content == '有js参数':
                    pass
            else:
                    TITLE_COUNT_TOTAL.append(title_content)


            if TITLE_COUNT_TOTAL.count(title_content) == PAGE_REPEAT:

                match_rules_list.append(title_content)
            if title_rules != False:
                await CODE_200_PRINT(response, info_200, INFO_TYPE, TITLE_CONTENT, TITLE_RULES, info_server_200)
            else:
                response.close()

        else:

            title_content = '[' + 'None' + ']'
            title_rules = await re_tilte_rules(response, title_content)

            if title_rules != False:
                TITLE_RULES = color_one.yellow + '[' + str(title_rules) + ']' + color_one.end
                await CODE_200_PRINT(response, info_200, INFO_TYPE, title_content, TITLE_RULES, info_server_200)

async def CODE_200_PRINT(response , info_200 , info_type , title_content, TITLE_RULES, info_server_200):
        global DISPLAY_COUNT
        DISPLAY_COUNT+=1
        print('%-15s %-20s %s %s ' % (color_one.run + info_200 ,
                                                      info_type ,
                                                    TITLE_RULES,
                              color_one.purple + title_content + color_one.end))
        print('%s ' % (info_server_200))
        response.close()

async def CODE_302(payload,response,status_code):
    info_302 = color_one.green_blue + '[' + str(status_code) + ']' + color_one.end
    info_type = str(response.content_type)
    INFO_TYPE = color_one.green_blue + '[' + info_type + ']' + color_one.end
    info_server_302 = color_one.blue_good + color_one.blue  +URL_one + payload + color_one.end

    if info_type=='text/html':
        title_content = await title_Identify(response)
        TITLE_CONTENT = '[' + title_content + ']'
        title_rules = await re_tilte_rules_red(response, title_content)
        TITLE_RULES = color_one.yellow + '[' + str(title_rules) + ']' + color_one.end

        if title_content == 'title请求错误' and title_rules == None:
            TITLE_COUNT_TOTATL_RED.append(title_content)

        elif title_content == 'title请求错误' or title_content == None:
            pass
        elif title_content == '有js参数':
            pass
        else:
            TITLE_COUNT_TOTATL_RED.append(title_content)

        if TITLE_COUNT_TOTATL_RED.count(title_content) == PAGE_REPEAT:
            match_rules_list.append(title_content)

        if title_rules != False:
             await CODE_302_PRINT(response, info_302, INFO_TYPE, TITLE_CONTENT, TITLE_RULES, info_server_302)
        else:
            response.close()

    else:
        title_content = color_one.purple + color_one.green + '[' + 'None' + ']' + color_one.end
        title_rules = await re_tilte_rules(response, title_content)

        if title_rules != False:
            TITLE_RULES = color_one.yellow + '[' + str(title_rules) + ']' + color_one.end
            await CODE_302_PRINT(response, info_302, INFO_TYPE, title_content, TITLE_RULES, info_server_302)


async def CODE_302_PRINT(response , info_302 , info_type , title_content, title_rules, info_server_302):
        global DISPLAY_COUNT
        DISPLAY_COUNT += 1
        print('%-15s %-20s %s %s ' % (color_one.run +  info_302 ,
                                         info_type,
                                        title_rules,
                     color_one.purple + title_content + color_one.end))
        print('%s ' % (info_server_302))
        response.close()

async def CODE_400(payload,response,status_code):
        info_400 = color_one.red + '[' + str(status_code) + ']' + color_one.end
        info_type =  str(response.content_type)
        INFO_TYPE = color_one.green_blue + '[' + info_type + ']' + color_one.end
        info_server_400 = color_one.bad + color_one.red + URL_one + payload + color_one.end

        if info_type == 'text/html':
            title_content = await title_Identify(response)
            TITLE_CONTENT = '[' + title_content + ']'
            title_rules = await re_tilte_rules(response, title_content)
            TITLE_RULES = color_one.yellow + '[' + str(title_rules) + ']' + color_one.end

            if title_content == 'title请求错误' and title_rules == None:
                TITLE_COUNT_TOTATL_RED.append(title_content)

            elif title_content == 'title请求错误' or title_content == None:
                    pass
            elif title_content == '有js参数':
                    pass
            else:
                TITLE_COUNT_TOTATL_RED.append(title_content)

            if TITLE_COUNT_TOTATL_RED.count(title_content) == PAGE_REPEAT:
                match_rules_list.append(title_content)
            if title_rules != False:
                await CODE_200_PRINT(response, info_400, INFO_TYPE, TITLE_CONTENT, TITLE_RULES, info_server_400)
            else:
                response.close()

        else:
            title_content = color_one.purple +'[' + 'None' + ']' + color_one.end
            title_rules = await re_tilte_rules_red(response, title_content)

            if title_rules != False:
                TITLE_RULES = color_one.yellow + '[' + str(title_rules) + ']' + color_one.end
                await CODE_200_PRINT(response, info_400, INFO_TYPE, title_content,TITLE_RULES, info_server_400)

async def CODE_400_PRINT(response , info_400 , info_type , title_content, TITLE_RULES, info_server_400):
        global DISPLAY_COUNT
        DISPLAY_COUNT += 1
        print('%-15s %-20s %s %s ' % (color_one.run +
                                      info_400  ,
                                      info_type,
                                      title_rules,
                                    color_one.purple + title_content + color_one.end))
        print('%s ' % (info_server_400))
        response.close()



async def CODE_Other(payload,response,status_code):
    info_other = color_one.red + '[' + str(status_code) + ']' + color_one.end

    info_type =  str(response.content_type)
    INFO_TYPE = color_one.green_blue + '[' + info_type + ']' +color_one.end
    info_server_other = color_one.info + color_one.yellow  + URL_one + payload + color_one.end

    if info_type == 'text/html':
        title_content = await title_Identify(response)
        TITLE_CONTENT = '[' + title_content + ']'
        title_rules = await re_tilte_rules_red(response, title_content)
        TITLE_RULES = color_one.yellow + '[' + str(title_rules) + ']' + color_one.end
        if title_content=='title请求错误' and title_rules == None:
            TITLE_COUNT_TOTATL_RED.append(title_content)

        elif title_content == 'title请求错误' or title_content == None:
            pass
        elif title_content == '有js参数':
            pass
        else:
            TITLE_COUNT_TOTATL_RED.append(title_content)

        if TITLE_COUNT_TOTATL_RED.count(title_content) == PAGE_REPEAT:
            match_rules_list.append(title_content)
        if title_rules != False:
            await CODE_Others_PRINT(response, info_other, INFO_TYPE, TITLE_CONTENT, TITLE_RULES, info_server_other)
        else:
            response.close()

    else:
        title_content = color_one.purple + '[' + 'None' + ']' + color_one.end
        title_rules = await re_tilte_rules(response, title_content)
        if title_rules != False:
            TITLE_RULES = color_one.yellow + '[' + str(title_rules) + ']' + color_one.end
            await CODE_Others_PRINT(response, info_other, INFO_TYPE, title_content, TITLE_RULES, info_server_other)

async def CODE_Others_PRINT(response , info_other , info_type , title_content, title_rules, info_server_other):
        global DISPLAY_COUNT
        DISPLAY_COUNT += 1
        print('%-15s %-20s %s %s ' % (color_one.run +
                                        info_other ,
                                         info_type,
                                        title_rules,
                 color_one.purple + title_content +   color_one.end))
        print('%s ' % (info_server_other))
        response.close()


#title识别
async  def title_Identify(responese):
            global Title_Soup
            global TITLE_COUNT_SCRIPT
            global TITLE_COUNT_ERROR
            try:
                Title_Soup = BeautifulSoup(await responese.text(),'lxml')
                if Title_Soup != None:
                    return Title_Soup.title.string.replace('\n', ''). \
                replace('\r', '').replace('\t', '')
                else:
                    return  None

            except  Exception as e:
                try:
                    if Title_Soup.find_all('script') or Title_Soup.find_all('SCRIPT'):
                            TITLE_COUNT_SCRIPT.append(str(Title_Soup))

                            #Determine whether the page is the same
                            if TITLE_COUNT_SCRIPT.count(str(Title_Soup)) >= 5:
                                    return False
                            else:
                                    return  '有js参数'
                    else:
                        TITLE_COUNT_ERROR.append(str(Title_Soup))
                        if TITLE_COUNT_ERROR.count(str(Title_Soup)) >= 5:
                                    return False
                        else:
                                    return  'title请求错误'

                except Exception as e:
                                    return 'title请求错误'

#read rules file  + limit_asyncio
def read_rules_file():
    global match_rules_list
    global ASYNCIO_COUNT
    global PAGE_REPEAT
    global TIMEOUT
    match_rules_list = []
    CONFING_READ.read('./config/conf.conf',encoding='utf-8')
    for READ_CONF in CONFING_READ['match_rules'].values():
        match_rules_list.append(str(READ_CONF))
    ASYNCIO_COUNT = CONFING_READ['limit_asyncio'].getint('limit_count')
    PAGE_REPEAT = CONFING_READ['titlte_repeat'].getint('repeat')
    TIMEOUT = CONFING_READ['time_out_dir'].getfloat('time_out_dir')


#read file limit byte length(200)
def READ_LIMIT_BYTE_LENGTH():
    global LIMIT_BYTE
    CONFING_READ.read('./config/conf.conf',encoding='utf-8')
    LIMIT_BYTE = CONFING_READ['limit_byte'].getint('limit')

#read file limit byte length(red)
def READ_LIMIT_BYTE_LENGTH_READ():
    global LIMIT_BYTE_RED
    CONFING_READ.read('./config/conf.conf',encoding='utf-8')
    LIMIT_BYTE_RED = CONFING_READ['limit_byte_red'].getint('limit')

#rules match
async def re_tilte_rules(response,title_content):
    global match_rules_list
    global LIMIT_BYTE
    if response.content_length != None:
        CONTNET_LENGTH = int(response.content_length)
        # limit bytes
        if CONTNET_LENGTH <= LIMIT_BYTE:
            return False
        #limit content
        elif title_content in match_rules_list:
            return False

        else:
            return  CONTNET_LENGTH
    else:
        if title_content in match_rules_list:
            return False
        else:
            return None



#return byte count
async def re_tilte_rules_red(response,title_content):
    global match_rules_list
    global LIMIT_BYTE_RED
    if response.content_length != None:
        CONTNET_LENGTH = int(response.content_length)

        # limit bytes
        if CONTNET_LENGTH <= LIMIT_BYTE_RED:
            return False

        #limit content
        elif title_content in match_rules_list:
            return False
        else:
            return  CONTNET_LENGTH
    else:
       if title_content in match_rules_list:
            return False
       else:
            return None


async def GET_PARSE(sem, client, bar_one, payload):
        global url_one
        async with sem:
            try:
                async with client.get(url=url_one+payload, headers=user_agent.user_agent(),
                        proxy=PROXY, ssl=False) as responese:
                    await CODE_SCAN(payload, responese)
            except Exception as error:
                pass
            bar_one()

async def scan(ASYNCIO_COUNT,PAYLOAD_LIST_TOTAL,COUNT_TOTAL):
            sem = asyncio.Semaphore(ASYNCIO_COUNT)
            tasks = []
            cookie_jar_one = aiohttp.CookieJar(unsafe = True)
            timeout = aiohttp.ClientTimeout(total = TIMEOUT)
            CONE_ONE = aiohttp.TCPConnector(limit = ASYNCIO_COUNT)
            with alive_bar(COUNT_TOTAL) as bar_one:

                async with aiohttp.ClientSession(cookie_jar = cookie_jar_one,timeout = timeout,connector = CONE_ONE) as client:

                    for payload in PAYLOAD_LIST_TOTAL:
                                tasks.append(asyncio.create_task(GET_PARSE(sem,client,bar_one,payload)))
                    await asyncio.wait(tasks)
                info_count = str(DISPLAY_COUNT)
                print('\n' +color_one.green+ '共找多{}个有用的信息'.format(info_count) +color_one.end)

def worker_ONE(ASYNCIO_COUNT,PAYLOAD_LIST,COUNT):
    global loop
    loop = None
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:

        selector = selectors.SelectSelector()
        loop = asyncio.SelectorEventLoop(selector)
        loop.run_until_complete(scan(ASYNCIO_COUNT,PAYLOAD_LIST, COUNT))
    except KeyboardInterrupt:
        print(color_one.red + "\nCTRL+C detected, Exit..." + color_one.end)
    finally:
        if loop != None:
            loop.close()



def main():
        PATH_URL()
        url_to_ip(url_one)
        URL_one_display()

        if Host_identification(url_one) != False:
            # 加载rules
            read_rules_file()
            #加载LIMIT_BYTE
            READ_LIMIT_BYTE_LENGTH()
            #加载LIMIT_BYTE_RED
            READ_LIMIT_BYTE_LENGTH_READ()
            global TYPES_OF
            TYPES_OF=''
            ARGS_ONE = args_one.split(',')
            for ARGS_TOTAL in ARGS_ONE:
                TYPES_OF+=ARGS_TOTAL+' '


            print(color_one.red + '[DEBUG' + color_one.yellow + '目录探测中....' + color_one.end)
            print((f'{color_one.green}================================================================================================={color_one.end}'))
            print(color_one.info + color_one.blue +  'Targets : ' +color_one.yellow + URL_one  + color_one.end + '\t\t' + color_one.yellow + 'TYPES_OF:' +  color_one.purple + TYPES_OF + color_one.end)
            if PROXY==None:
                pass
            else:
                print(color_one.info + color_one.yellow + 'proxy:' + PROXY + color_one.end)

            if 'dir' in ARGS_ONE:
                DIR_PATH = 'dir' + '.txt'
                print(color_one.run + color_one.blue +'start dir字典扫描'+color_one.end)
                PAYLOAD_LIST, COUNT = READ_FILE_TOTAL_LOWER(DIR_PATH)
                worker_ONE(ASYNCIO_COUNT,PAYLOAD_LIST,COUNT)

            elif 'DIR' in ARGS_ONE:
                DIR_PATH_UPPER = 'DIR' + '.txt'
                print(color_one.run + color_one.blue  + 'start DIR字典扫描' + color_one.end)
                PAYLOAD_LIST_DIR_DEEP,COUNT_DEEP_DIR = READ_FILE_TOTAL_UPPER(DIR_PATH_UPPER)
                worker_ONE(ASYNCIO_COUNT,PAYLOAD_LIST_DIR_DEEP,COUNT_DEEP_DIR)

            elif 'php' in ARGS_ONE:
                DIR_PATH = 'php' + '.txt'
                print(color_one.run + color_one.blue + 'start php字典扫描' + color_one.end)
                PAYLOAD_LIST_PHP, COUNT_PHP = READ_FILE_TOTAL_LOWER(DIR_PATH)
                worker_ONE(ASYNCIO_COUNT,PAYLOAD_LIST_PHP, COUNT_PHP)

            elif 'PHP' in ARGS_ONE:
                DIR_PATH_UPPER = 'PHP' + '.txt'
                print(color_one.run + color_one.blue + 'start PHP字典扫描' + color_one.end)
                PAYLOAD_LIST_ASP, COUNT_ASP = READ_FILE_TOTAL_UPPER(DIR_PATH_UPPER)
                worker_ONE(ASYNCIO_COUNT, PAYLOAD_LIST_ASP, COUNT_ASP)

            elif 'asp' in ARGS_ONE:
                DIR_PATH = 'asp' + '.txt'
                print(color_one.run + color_one.blue + 'start asp字典扫描' + color_one.end)
                PAYLOAD_LIST_ASP, COUNT_ASP = READ_FILE_TOTAL_LOWER(DIR_PATH)
                worker_ONE(ASYNCIO_COUNT,PAYLOAD_LIST_ASP, COUNT_ASP)

            elif 'ASP' in ARGS_ONE:
                DIR_PATH_UPPER = 'ASP' + '.txt'
                print(color_one.run + color_one.blue + 'start ASP字典扫描' + color_one.end)
                PAYLOAD_LIST_ASP, COUNT_ASP = READ_FILE_TOTAL_UPPER(DIR_PATH_UPPER)
                worker_ONE(ASYNCIO_COUNT,PAYLOAD_LIST_ASP, COUNT_ASP)

            elif 'aspx' in ARGS_ONE:
                DIR_PATH = 'aspx' + '.txt'
                print(color_one.run + color_one.blue + 'start aspx字典扫描' + color_one.end)
                PAYLOAD_LIST_ASPX, COUNT_ASPX = READ_FILE_TOTAL_LOWER(DIR_PATH)
                worker_ONE(ASYNCIO_COUNT,PAYLOAD_LIST_ASPX, COUNT_ASPX)

            elif 'ASPX' in ARGS_ONE:
                DIR_PATH_UPPER = 'ASPX' + '.txt'
                print(color_one.run + color_one.blue + 'start ASPX字典扫描' + color_one.end)
                PAYLOAD_LIST_ASPX, COUNT_ASPX = READ_FILE_TOTAL_UPPER(DIR_PATH_UPPER)
                worker_ONE(ASYNCIO_COUNT,PAYLOAD_LIST_ASPX, COUNT_ASPX)

            elif 'jsp'  in ARGS_ONE:
                DIR_PATH = 'jsp' + '.txt'
                print(color_one.run + color_one.blue +'start jsp字典扫描' + color_one.end)
                PAYLOAD_LIST_JSP, COUNT_JSP = READ_FILE_TOTAL_LOWER(DIR_PATH)
                worker_ONE(ASYNCIO_COUNT,PAYLOAD_LIST_JSP, COUNT_JSP)

            elif 'JSP'  in ARGS_ONE:
                DIR_PATH_UPPER = 'JSP' + '.txt'
                print(color_one.run + color_one.blue +'start JSP字典扫描' + color_one.end)
                PAYLOAD_LIST_JSP, COUNT_JSP = READ_FILE_TOTAL_UPPER(DIR_PATH_UPPER)
                worker_ONE(ASYNCIO_COUNT,PAYLOAD_LIST_JSP, COUNT_JSP)

            elif 'mdb' in ARGS_ONE:
                DIR_PATH = 'mdb' + '.txt'
                print(color_one.run + color_one.blue + 'start mdb字典扫描' + color_one.end)
                PAYLOAD_LIST_MDB, COUNT_MDB = READ_FILE_TOTAL_LOWER(DIR_PATH)
                worker_ONE(ASYNCIO_COUNT,PAYLOAD_LIST_MDB, COUNT_MDB)

            elif 'admin' in ARGS_ONE:
                DIR_PATH = 'admin' + '.txt'
                print(color_one.run + color_one.blue + 'start admin字典扫描' + color_one.end)
                PAYLOAD_LIST_MDB, COUNT_MDB = READ_FILE_TOTAL_LOWER(DIR_PATH)
                worker_ONE(ASYNCIO_COUNT, PAYLOAD_LIST_MDB, COUNT_MDB)

            else:
                print(color_one.red+"请输入正确的字典格式!" + color_one.red)
                return False
        else:
            pass
