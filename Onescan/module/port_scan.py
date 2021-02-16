import asyncio
import socket
import selectors
import configparser
import re
from module import color_one
from alive_progress import alive_bar

url_one = ' '
ARGS_PARAMETER = ' '
ASYNCIO_COUNT = 0
PORT_LIST_TOTAL = []
TIMEOUT = 0

CONFIG_READ = configparser.ConfigParser()


# 主机识别
def Host_identification(url_one):
    if re.search(r'http://', url_one) or re.search(r'https://', url_one):
        return url_to_ip(url_one)

    elif re.search(r'^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}', url_one):
        return url_one

    else:
        print(color_one.red + '错误的地址' + color_one.end)
        return False


async def scan_host(BAR, host, port, semaphore):
    global writer
    writer = None
    async with semaphore:
        BAR()
        try:
            fut =  asyncio.open_connection(host, port)
            reader, writer = await asyncio.wait_for(fut, timeout=TIMEOUT)
            if writer:
                data = await  asyncio.wait_for(reader.read(128),timeout=TIMEOUT)
                await PRINT_RESULTS(host, data, port)
                writer.close()
        except Exception as e:
            if writer!=None:
                writer.close()




async def PRINT_RESULTS(host, data, port):
    DATA_RECV = ' '
    INFO_PORTS = color_one.green + color_one.yellow + str(port) + color_one.end
    INFO_BANNER = color_one.green + '[tcp/open]' + color_one.end
    DATA_HOST = color_one.blue_good + host + color_one.end
    if bool(data)!= False:
        DATA_RECV = color_one.purple + '[' + str(data.decode('utf-8')) + ']' + color_one.end
    else:
        pass
    print('%-28s %-10s %-20s %s' % (DATA_HOST, INFO_PORTS, INFO_BANNER, DATA_RECV))


async def run_scan_host(host, PORT_LIST):
    semaphore = asyncio.Semaphore(ASYNCIO_COUNT)
    task_list = []
    PAYLOAD_COUNT = []
    COUNT = 0
    for payload_count in PORT_LIST:
        PAYLOAD_COUNT.append(payload_count)
        COUNT += 1
    with alive_bar(COUNT) as BAR:
        for port in PAYLOAD_COUNT:
            task_list.append(asyncio.create_task(scan_host(BAR, host, port, semaphore)))

        await asyncio.wait(task_list)


def url_to_ip(url):
    domain = url.split('/')[0] if '://' not in url else url.split('//')[1].split('/')[0]
    domain = domain.split(':')[0] if ':' in domain else domain
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except Exception as e:
        return False


def READ_CONFIG_FILE():
    global ASYNCIO_COUNT
    global TIMEOUT
    CONFIG_READ.read('./config/conf.conf', encoding='utf-8')
    ASYNCIO_COUNT = CONFIG_READ['limit_asyncio'].getint('limit_count')
    TIMEOUT = CONFIG_READ['time_out'].getfloat('timeout')


def READ_PORT_LIST():
    with open('./dict/port.txt') as file:
        for PORT_LIST in file:
            PORT_LIST_TOTAL.append(PORT_LIST.strip('\n'))


def WORK_ONE(host, PORT_LIST):
    global loop
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        selector = selectors.SelectSelector()
        loop = asyncio.SelectorEventLoop(selector)
        loop.run_until_complete(run_scan_host(host, PORT_LIST))

    except KeyboardInterrupt:
        print(color_one.red + "\nCTRL+C detected, Exit..." + color_one.end)
    finally:
        loop.close()


# 默认端口扫描
def main():
    # 加载配置文件
    READ_CONFIG_FILE()
    # 加载端口列表
    READ_PORT_LIST()
    host = Host_identification(url_one)
    if host!=False:
        print(color_one.red + '[DEBUG' + color_one.yellow + '端口扫描....' + color_one.end)
        print((
            f'{color_one.green}================================================================================================={color_one.end}'))
        print(color_one.yellow + 'Target: ' + color_one.blue + host + color_one.end + '\n')
        WORK_ONE(host, PORT_LIST_TOTAL)


def run():
    host = Host_identification(url_one)
    if host!=False:
        print(color_one.red + '[DEBUG' + color_one.yellow + '自定义端口扫描....' + color_one.end)
        print((
            f'{color_one.green}================================================================================================={color_one.end}'))
        print(color_one.yellow + 'Target: ' + color_one.blue + host + color_one.end + '\n')
        # 保存端口列表
        LIST_PORT_RUN_TOTAL = []

        # 加载配置文件
        READ_CONFIG_FILE()
        LIST_PORT_RUN = ARGS_PARAMETER.split(',')
        for LIST_PORT in LIST_PORT_RUN:
            if re.search(r'-', str(LIST_PORT)):
                start_port, end_port = LIST_PORT.split('-')
                for PORT_SPLIT in range(int(start_port), int(end_port)):
                    LIST_PORT_RUN_TOTAL.append(PORT_SPLIT)

            else:
                LIST_PORT_RUN_TOTAL.append(LIST_PORT)
        WORK_ONE(host, LIST_PORT_RUN_TOTAL)
    else:
        pass