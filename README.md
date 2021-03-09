# ONESCAN
修改了C段的request同步库为aiohttp异步库速度更快
轻量扫描器
使用参考文章
https://blog.csdn.net/qq_46804551/article/details/113824061


usage: One.py -u http://www.example.com/ -d dir -c ...

optional arguments:
  -h, --help    show this help message and exit
  -u U          指定url 或 ip 如:-u http://www.baidu.com
  -c            C段扫描
  -j            js接口扫描
  -js           js接口扫描深度探测
  -d D          目录扫描 如: -d dir
  -p            默认的端口扫描
  -P P          指定端口扫描 如 1-100,445
  -poc          漏洞验证
  -proxy PROXY  代理设置 例如:http://127.0.0.1:1080(只支持http)
