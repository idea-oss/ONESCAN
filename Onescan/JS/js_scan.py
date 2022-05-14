#!/usr/bin/env python3
# encoding:utf8
import requests, sys, re
import multiprocessing
from requests.packages import urllib3
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from module import color_one
from multiprocessing import Pool,Lock
import queue
URL=''
def extract_URL(JS):
    pattern_raw = r"""
	  (?:"|')                               # Start newline delimiter
	  (
	    ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
	    [^"'/]{1,}\.                        # Match a domainname (any character + dot)
	    [a-zA-Z]{2,}[^"']{0,})              # The domainextension and/or path
	    |
	    ((?:/|\.\./|\./)                    # Start with /,../,./
	    [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be...
	    [^"'><,;|()]{1,})                   # Rest of the characters can't be
	    |
	    ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
	    [a-zA-Z0-9_\-/]{1,}                 # Resource name
	    \.(?:[a-zA-Z]{1,4}|action)          # Rest + extension (length 1-4 or action)
	    (?:[\?|/][^"|']{0,}|))              # ? mark with parameters
	    |
	    ([a-zA-Z0-9_\-]{1,}                 # filename
	    \.(?:php|asp|aspx|jsp|json|
	         action|html|js|txt|xml)             # . + extension
	    (?:\?[^"|']{0,}|))                  # ? mark with parameters
	  )
	  (?:"|')                               # End newline delimiter
	"""
    pattern = re.compile(pattern_raw, re.VERBOSE)
    result = re.finditer(pattern, str(JS))
    if result==None:
        return None
    js_url = []
    return [match.group().strip('"').strip("'") for match in result
            if match.group() not in js_url]
def Extract_html(URL):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"}
    try:
        raw = requests.get(URL, headers=header, timeout=3, verify=False)
        raw = raw.content.decode("utf-8", "ignore")
        return raw
    except:
        return None



def process_url(URL, re_URL):
    black_url = ["javascript:"]
    URL_raw = urlparse(URL)
    ab_URL = URL_raw.netloc
    host_URL = URL_raw.scheme
    if re_URL[0:2]=="//":
        result = host_URL + ":" + re_URL
    elif re_URL[0:4]=="http":
        result = re_URL
    elif re_URL[0:2]!="//" and re_URL not in black_url:
        if re_URL[0:1]=="/":
            result = host_URL + "://" + ab_URL + re_URL
        else:
            if re_URL[0:1]==".":
                if re_URL[0:2]=="..":
                    result = host_URL + "://" + ab_URL + re_URL[2:]
                else:
                    result = host_URL + "://" + ab_URL + re_URL[1:]
            else:
                result = host_URL + "://" + ab_URL + "/" + re_URL
    else:
        result = URL
    return result


def find_last(string, str):
    positions = []
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position==-1: break
        last_position = position
        positions.append(position)
    return positions


def find_by_url(url, js=False):
    if js==False:
        try:
            url
        except:
            print("Please specify a URL like https://www.baidu.com")
        html_raw = Extract_html(url)
        if html_raw==None:
            print("Fail to access " + url)
            return None
        html = BeautifulSoup(html_raw, "html.parser")
        html_scripts = html.findAll("script")
        script_array = {}
        script_temp = ""
        for html_script in html_scripts:
            script_src = html_script.get("src")
            if script_src==None:
                script_temp += html_script.get_text() + "\n"
            else:
                purl = process_url(url, script_src)
                script_array[purl] = Extract_html(purl)
        script_array[url] = script_temp
        allurls = []
        for script in script_array:
            temp_urls = extract_URL(script_array[script])
            if len(temp_urls)==0: continue
            for temp_url in temp_urls:
                allurls.append(process_url(script, temp_url))
        result = []
        for singerurl in allurls:
            url_raw = urlparse(url)
            domain = url_raw.netloc
            positions = find_last(domain, ".")
            miandomain = domain
            if len(positions) > 1: miandomain = domain[positions[-2] + 1:]
            suburl = urlparse(singerurl)
            subdomain = suburl.netloc
            if miandomain in subdomain or subdomain.strip()=="":
                if singerurl.strip() not in result:
                    result.append(singerurl)
        return result
    return sorted(set(extract_URL(Extract_html(url)))) or None


def find_subdomain(urls, mainurl):
    url_raw = urlparse(mainurl)
    domain = url_raw.netloc
    miandomain = domain
    positions = find_last(domain, ".")
    if len(positions) > 1: miandomain = domain[positions[-2] + 1:]
    subdomains = []
    for url in urls:
        suburl = urlparse(url)
        subdomain = suburl.netloc
        if subdomain.strip()=="": continue
        if miandomain in subdomain:
            if subdomain not in subdomains:
                subdomains.append(subdomain)
    return subdomains
def find_by_url_deep(url):
    q = queue.Queue()
    html_raw = Extract_html(url)
    if html_raw==None:
        print("Fail to access " + url)
        return None
    html = BeautifulSoup(html_raw, "html.parser")
    html_as = html.findAll("a")
    links = []
    for html_a in html_as:
        src = html_a.get("href")
        if src=="" or src==None: continue
        link = process_url(url, src)
        if link not in links:
            links.append(link)
    if links==[]: return None
    print(color_one.red+"ALL Find " + str(len(links)) + " links"+color_one.end)
    count=int(len(links))
    urls = []
    i = len(links)
    print(color_one.yellow + "url:" + url + color_one.end)
    for link in links:
        temp_urls = find_by_url(link)
        if temp_urls==None: continue
        print(color_one.yellow+"Find"+'   ' + str(len(temp_urls))+color_one.end + " url in " + link)
        for temp_url in temp_urls:
            if temp_url not in urls:
                urls.append(temp_url)
    i -= 1
    return urls

def giveresult(urls, domian):
    if urls==None:
        return None
    print("Find " + str(len(urls)) + " URL:")
    content_url = ""
    content_subdomain = ""
    for url in urls:
        content_url += url + "\n"
        print(url)
    subdomains = find_subdomain(urls, domian)
    print("\nFind"+ str(len(subdomains)) + " Subdomain:")
    print(color_one.green_blue+'Url\t\t\t\t\t\t\t'+'状态\t\t\t\t\t\t\t'+'Banner')
    _threading_list=[]
    _multiprocessing=multiprocessing.Pool(6)

    for subdomain in subdomains:
        subdomain=subdomain.strip('\n')
        _multiprocessing.apply_async(par_subdomain,args=(subdomain,))
    _multiprocessing.close()
    _multiprocessing.join()
def par_subdomain(subdomain):

    if re.search('http',subdomain) or re.search('https',subdomain):
        subdomain=subdomain
    else:
        subdomain='http://'+subdomain
    results=requests.get(subdomain)
    soup=BeautifulSoup(results.content,'lxml')
    if results.status_code==200:
        info_titlt= str(color_one.green+subdomain+'\t\t\t\t\t'+color_one.green+str(results.status_code)+'\t\t\t\t\t'+
              color_one.yellow+str(soup.title.string.replace('\n', '').replace('\r', '').replace('\t', '')).strip('\n')
              +color_one.end)
        if 'Server' in results.headers:
            info_server=(color_one.green_blue+'['+results.headers['Server']+']'+color_one.end)
        else:
            info_server=color_one.red+'None'+color_one.end
        print(info_titlt+info_server)
    else:
        info_title=str(color_one.red+subdomain+'\t\t\t\t\t'+color_one.red+str(results.status_code)+'\t\t\t\t\t'+color_one.yellow+
        str(soup.title.string.replace('\n', '').replace('\r', '').replace('\t', '')).strip('\n')+color_one.end)
        if 'Server' in results.headers:
            info_server=str(color_one.green_blue+'['+results.headers['Server']+']'+color_one.end)
        else:
            info_server=color_one.red+'None'+color_one.end
        print(info_title+ info_server)

def Host_identification(URL_ONE):
    global  URL
    if re.search(r'http://',URL_ONE) or re.search(r'https://',URL_ONE):
           return URL

    elif re.search(r'^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}',URL_ONE):
             URL = ('http://'+URL_ONE).strip('\n')

    else:
        print(color_one.red + '错误的地址' + color_one.end)
        return False

def main():
    if Host_identification(URL) != False:
        urllib3.disable_warnings()
        print(''''\033[91m[DEBUG\33[0m\033[93mJS接口探测中....\33[0m''')
        print((f'{color_one.green}================================================================================================={color_one.end}'))
        print(color_one.yellow + 'Target: ' + color_one.blue + URL + color_one.end + '\n')
        urls = find_by_url(URL)
        giveresult(urls, URL)
def run():
    if Host_identification(URL) != False:
        urllib3.disable_warnings()
        print(''''\033[91m[DEBUG\33[0m\033[93mJS接口深度探测中....\33[0m''')
        print((f'{color_one.green}================================================================================================={color_one.end}'))
        print(color_one.yellow + 'Target: ' + color_one.blue + URL + color_one.end + '\n')
        urls = find_by_url_deep(URL)
        giveresult(urls,URL)
